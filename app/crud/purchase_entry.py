from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.purchase_entry import PurchaseEntry, PurchaseEntryItem
from app.models.product import Product
from app.schemas.purchase_entry import PurchaseEntryCreate, PurchaseEntryUpdate
from datetime import datetime

def get_purchase_entry(db: Session, purchase_id: int):
    return db.query(PurchaseEntry).filter(PurchaseEntry.id == purchase_id).first()

def get_purchase_entries(db: Session, skip: int = 0, limit: int = 100, search: str = ""):
    query = db.query(PurchaseEntry)
    if search:
        query = query.filter(PurchaseEntry.purchase_number.ilike(f"%{search}%"))
    return query.order_by(desc(PurchaseEntry.id)).offset(skip).limit(limit).all()

def count_purchase_entries(db: Session, search: str = ""):
    query = db.query(PurchaseEntry)
    if search:
        query = query.filter(PurchaseEntry.purchase_number.ilike(f"%{search}%"))
    return query.count()

def create_purchase_entry(db: Session, entry: PurchaseEntryCreate):
    db_entry = PurchaseEntry(
        purchase_number=entry.purchase_number,
        purchase_date=entry.purchase_date,
        supplier_id=entry.supplier_id,
        subtotal=entry.subtotal,
        grand_total=entry.grand_total,
        created_by_id=entry.created_by_id
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    # Add Items
    for item in entry.line_items:
        db_item = PurchaseEntryItem(
            purchase_entry_id=db_entry.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
            amount=item.amount
        )
        db.add(db_item)
        
        if item.product_id:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.quantity = (product.quantity or 0.0) + item.quantity
    
    db.commit()
    db.refresh(db_entry)
    return db_entry

def update_purchase_entry(db: Session, entry_id: int, entry_update: PurchaseEntryUpdate):
    db_entry = get_purchase_entry(db, entry_id)
    if not db_entry:
        return None
    
    update_data = entry_update.dict(exclude_unset=True)
    
    # Handle line items separately
    if "line_items" in update_data:
        # Revert existing stock
        old_items = db.query(PurchaseEntryItem).filter(PurchaseEntryItem.purchase_entry_id == entry_id).all()
        for old_item in old_items:
            if old_item.product_id:
                product = db.query(Product).filter(Product.id == old_item.product_id).first()
                if product:
                    product.quantity = (product.quantity or 0.0) - old_item.quantity

        # Delete existing
        db.query(PurchaseEntryItem).filter(PurchaseEntryItem.purchase_entry_id == entry_id).delete()
        # Add new
        line_items = update_data.pop("line_items")
        for item in line_items:
             db_item = PurchaseEntryItem(
                purchase_entry_id=entry_id,
                product_id=item.get("product_id"),
             
                quantity=item.get("quantity"),
                price=item.get("price", 0.0),
 
                amount=item.get("amount", 0.0)
            )
             db.add(db_item)
             
             product_id = item.get("product_id")
             if product_id:
                 product = db.query(Product).filter(Product.id == product_id).first()
                 if product:
                     product.quantity = (product.quantity or 0.0) + item.get("quantity", 0.0)

    # Update other fields
    for key, value in update_data.items():
        setattr(db_entry, key, value)
    
    db.commit()
    db.refresh(db_entry)
    return db_entry

def delete_purchase_entry(db: Session, entry_id: int):
    db_entry = get_purchase_entry(db, entry_id)
    if db_entry:
        for old_item in db_entry.line_items:
            if old_item.product_id:
                product = db.query(Product).filter(Product.id == old_item.product_id).first()
                if product:
                    product.quantity = (product.quantity or 0.0) - old_item.quantity
                    
        db.delete(db_entry)
        db.commit()
    return db_entry

def get_next_purchase_number(db: Session):
    last_entry = db.query(PurchaseEntry).order_by(desc(PurchaseEntry.id)).first()
    if not last_entry:
        return f"PUR-{datetime.now().year}-1000"
    
    try:
        parts = last_entry.purchase_number.split("-")
        last_num = int(parts[-1])
        return f"PUR-{datetime.now().year}-{last_num + 1}"
    except:
        return f"PUR-{datetime.now().year}-{last_entry.id + 1000}"
