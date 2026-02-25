from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base

class PurchaseEntry(Base):
    id = Column(Integer, primary_key=True, index=True)
    purchase_number = Column(String(50), unique=True, index=True, nullable=False)
    purchase_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    
    subtotal = Column(Float, default=0.0)
    grand_total = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    supplier = relationship("Supplier", backref="purchase_entries")
    created_by = relationship("User", backref="purchase_entries")
    line_items = relationship("PurchaseEntryItem", back_populates="purchase_entry", cascade="all, delete-orphan")


class PurchaseEntryItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    purchase_entry_id = Column(Integer, ForeignKey("purchaseentry.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True)
    
    
    quantity = Column(Float, default=1.0)
    price = Column(Float, default=0.0)
    amount = Column(Float, default=0.0)
    
    purchase_entry = relationship("PurchaseEntry", back_populates="line_items")
    product = relationship("Product")
