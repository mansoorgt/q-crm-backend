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
        db.add(db_obj)
        db.flush() # Get ID
        
        for item in line_items_data:
            db_item = InvoiceItem(**item, invoice_id=db_obj.id)
            db.add(db_item)
            
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
            
        # Optional: Check if invoice already exists for this quotation
        # existing = db.query(Invoice).filter(Invoice.quotation_id == quotation_id).first()
        # if existing: return existing

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
            tax_amount=quotation.tax_amount,
            grand_total=quotation.grand_total,
            balance_due=quotation.grand_total,
            notes=quotation.internal_notes,
            terms_conditions=quotation.terms_conditions
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
                total=q_item.total
            )
            db.add(inv_item)
            
        db.commit()
        db.refresh(invoice)
        return invoice

invoice = CRUDInvoice(Invoice)
