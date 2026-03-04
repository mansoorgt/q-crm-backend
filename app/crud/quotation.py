from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.quotation import Quotation, QuotationItem
from app.schemas.quotation import QuotationCreate, QuotationUpdate
from datetime import datetime

def get_quotation(db: Session, quotation_id: int):
    return db.query(Quotation).filter(Quotation.id == quotation_id).first()

def get_quotations(db: Session, skip: int = 0, limit: int = 100, search: str = ""):
    query = db.query(Quotation)
    if search:
        query = query.filter(Quotation.quotation_number.ilike(f"%{search}%"))
    return query.order_by(desc(Quotation.id)).offset(skip).limit(limit).all()

def count_quotations(db: Session, search: str = ""):
    query = db.query(Quotation)
    if search:
        query = query.filter(Quotation.quotation_number.ilike(f"%{search}%"))
    return query.count()

def create_quotation(db: Session, quotation: QuotationCreate):
    db_quotation = Quotation(
        quotation_number=quotation.quotation_number,
        quotation_date=quotation.quotation_date,
        valid_till=quotation.valid_till,
        status=quotation.status,
        customer_id=quotation.customer_id,
        contact_person_id=quotation.contact_person_id,
        inquiry_reference=quotation.inquiry_reference,
        billing_address=quotation.billing_address,
        subtotal=quotation.subtotal,
        discount_amount=quotation.discount_amount,
        tax_amount=quotation.tax_amount,
        grand_total=quotation.grand_total,
        sales_person_id=quotation.sales_person_id,
        terms_conditions=quotation.terms_conditions,
        internal_notes=quotation.internal_notes,
    )
    db.add(db_quotation)
    db.commit()
    db.refresh(db_quotation)
    
    # Add Items
    for item in quotation.line_items:
        db_item = QuotationItem(
            quotation_id=db_quotation.id,
            product_id=item.product_id,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            tax_rate=item.tax_rate,
            total=item.total
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_quotation)
    return db_quotation

def update_quotation(db: Session, quotation_id: int, quotation_update: QuotationUpdate):
    db_quotation = get_quotation(db, quotation_id)
    if not db_quotation:
        return None
    
    update_data = quotation_update.dict(exclude_unset=True)
    
    # Handle line items separately
    if "line_items" in update_data:
        # Delete existing
        db.query(QuotationItem).filter(QuotationItem.quotation_id == quotation_id).delete()
        # Add new
        line_items = update_data.pop("line_items")
        for item in line_items:
             db_item = QuotationItem(
                quotation_id=quotation_id,
                product_id=item.get("product_id"),
                description=item.get("description"),
                quantity=item.get("quantity"),
                unit_price=item.get("unit_price"),
                tax_rate=item.get("tax_rate"),
                stock_availability=item.get("stock_availability"), 
                total=item.get("total", 0.0) # Ensure total is passed or calculated
            )
             db.add(db_item)

    # Update other fields
    for key, value in update_data.items():
        setattr(db_quotation, key, value)
    
    db.commit()
    db.refresh(db_quotation)
    
    # Sync status to Inquiry if applicable
    if "status" in update_data and db_quotation.inquiry_reference:
        try:
            inquiry_id = int(db_quotation.inquiry_reference)
            from app.models.inquiry import Inquiry
            from app.models.quotation import QuotationStatus
            db_inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
            if db_inquiry:
                if db_quotation.status == QuotationStatus.APPROVED:
                    db_inquiry.status = "Won"
                elif db_quotation.status == QuotationStatus.REJECTED:
                    db_inquiry.status = "Lost"
                db.commit()
        except ValueError:
            pass # inquiry_reference is not an ID, ignore

    return db_quotation

def delete_quotation(db: Session, quotation_id: int):
    db_quotation = get_quotation(db, quotation_id)
    if db_quotation:
        db.delete(db_quotation)
        db.commit()
    return db_quotation

def get_next_quotation_number(db: Session):
    # Logic to get max ID or parse last number
    # Simple implementation: Count + 1000
    # Or find last record
    last_quote = db.query(Quotation).order_by(desc(Quotation.id)).first()
    if not last_quote:
        return f"QT-{datetime.now().year}-1000"
    
    # Try to parse increment
    try:
        parts = last_quote.quotation_number.split("-")
        last_num = int(parts[-1])
        return f"QT-{datetime.now().year}-{last_num + 1}"
    except:
        return f"QT-{datetime.now().year}-{last_quote.id + 1000}"
