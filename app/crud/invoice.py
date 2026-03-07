from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.invoice import Invoice, InvoiceItem, InvoiceStatus
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceItemCreate
from app.models.quotation import Quotation, QuotationStatus

class CRUDInvoice(CRUDBase[Invoice, InvoiceCreate, InvoiceUpdate]):
    def create_with_items(self, db: Session, *, obj_in: InvoiceCreate) -> Invoice:
        obj_in_data = obj_in.dict()
        line_items_data = obj_in_data.pop("line_items", [])
        
        db_obj = Invoice(**obj_in_data)
        if "balance_due" not in obj_in_data or obj_in_data["balance_due"] == 0:
            db_obj.balance_due = db_obj.grand_total
        db.add(db_obj)
        db.flush() # Get ID
        
        for item in line_items_data:
            db_item = InvoiceItem(**item, invoice_id=db_obj.id)
            db.add(db_item)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj
    def update(
        self,
        db: Session,
        *,
        db_obj: Invoice,
        obj_in: InvoiceUpdate
    ) -> Invoice:
        update_data = obj_in.dict(exclude_unset=True)
        
        # Handle line items separately
        if "line_items" in update_data:
            # Delete existing
            db.query(InvoiceItem).filter(InvoiceItem.invoice_id == db_obj.id).delete()
            # Add new
            line_items = update_data.pop("line_items")
            for item in line_items:
                 db_item = InvoiceItem(
                    invoice_id=db_obj.id,
                    product_id=item.get("product_id"),
                    description=item.get("description"),
                    quantity=item.get("quantity"),
                    unit_price=item.get("unit_price"),
                    tax_rate=item.get("tax_rate"),
                    stock_availability=item.get("stock_availability"), 
                    total=item.get("total", 0.0) # Ensure total is passed or calculated
                )
                 db.add(db_item)

        # Update other fields using CRUDBase update logic
        for field in update_data:
            setattr(db_obj, field, update_data[field])

        db_obj.balance_due = db_obj.grand_total - db_obj.amount_paid

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    def get_invoices(self, db: Session, *, skip: int = 0, limit: int = 100, search: str = "") -> List[Invoice]:
        query = db.query(Invoice)
        if search:
           query = query.filter(Invoice.invoice_number.ilike(f"%{search}%"))
        return query.order_by(Invoice.id.desc()).offset(skip).limit(limit).all()

    def count_invoices(self, db: Session, *, search: str = "") -> int:
        query = db.query(func.count(Invoice.id))
        if search:
            query = query.filter(Invoice.invoice_number.ilike(f"%{search}%"))
        return query.scalar()
        
    def get_next_invoice_number(self, db: Session) -> str:
        # Simple auto-increment logic: INV-0001
        last_invoice = db.query(Invoice).order_by(Invoice.id.desc()).first()
        if not last_invoice:
            return "INV-0001"
        
        try:
            last_num = int(last_invoice.invoice_number.split("-")[1])
            return f"INV-{last_num + 1:04d}"
        except:
             return f"INV-{last_invoice.id + 1:04d}"

    def create_from_quotation(self, db: Session, quotation_id: int) -> Invoice:
        quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
        if not quotation:
            raise ValueError("Quotation not found")
            
        # Check if invoice already exists for this quotation
        existing = db.query(Invoice).filter(Invoice.quotation_id == quotation_id).first()
        if existing:
            raise ValueError(f"Invoice already exists for this quotation:{existing.id}")

        invoice_number = self.get_next_invoice_number(db)
        
        invoice = Invoice(
            invoice_number=invoice_number,
            invoice_date=datetime.utcnow(),
            status=InvoiceStatus.DRAFT,
            quotation_id=quotation.id,
            customer_id=quotation.customer_id,
            subtotal=quotation.subtotal,
            discount_amount=quotation.discount_amount,
            shipping_amount=quotation.shipping_amount,
            bank_charges=quotation.bank_charges,
            tax_amount=quotation.tax_amount,
            grand_total=quotation.grand_total,
            balance_due=quotation.grand_total,
            notes=quotation.internal_notes
        )
        
        db.add(invoice)
        db.flush()
        
        for q_item in quotation.line_items:
            inv_item = InvoiceItem(
                invoice_id=invoice.id,
                product_id=q_item.product_id,
                description=q_item.description,
                quantity=q_item.quantity,
                unit_price=q_item.unit_price,
                tax_rate=q_item.tax_rate,
                total=q_item.total,
                stock_availability=q_item.stock_availability,
            )
            db.add(inv_item)
            
        db.commit()
        db.refresh(invoice)
        return invoice

    def add_payment(self, db: Session, invoice_id: int, payment_in: "InvoicePaymentCreate") -> "InvoicePayment":
        from app.models.invoice import InvoicePayment
        
        invoice = self.get(db, id=invoice_id)
        if not invoice:
            raise ValueError("Invoice not found")
            
        payment = InvoicePayment(
            invoice_id=invoice_id,
            amount=payment_in.amount,
            payment_method=payment_in.payment_method,
            reference_number=payment_in.reference_number,
            notes=payment_in.notes
        )
        db.add(payment)
        
        # Update invoice amounts
        invoice.amount_paid += payment_in.amount
        invoice.balance_due = invoice.grand_total - invoice.amount_paid
        
        # Auto update status if fully paid
        if invoice.balance_due <= 0:
            invoice.status = InvoiceStatus.PAID
            
        db.commit()
        db.refresh(payment)
        return payment

    def delete_payment(self, db: Session, invoice_id: int, payment_id: int):
        from app.models.invoice import InvoicePayment
        
        payment = db.query(InvoicePayment).filter(
            InvoicePayment.id == payment_id,
            InvoicePayment.invoice_id == invoice_id
        ).first()
        
        if not payment:
            raise ValueError("Payment not found")
            
        invoice = self.get(db, id=invoice_id)
        if invoice:
            invoice.amount_paid -= payment.amount
            invoice.balance_due = invoice.grand_total - invoice.amount_paid
            
            # Revert status if we were Paid but now we have balance
            if invoice.balance_due > 0 and invoice.status == InvoiceStatus.PAID:
                invoice.status = InvoiceStatus.SENT # or another appropriate status
                
        db.delete(payment)
        db.commit()
        return True

invoice = CRUDInvoice(Invoice)
