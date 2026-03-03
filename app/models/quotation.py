from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.base_class import Base

class QuotationStatus(str, enum.Enum):
    DRAFT = "Draft"
    SENT = "Sent"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class Quotation(Base):
    id = Column(Integer, primary_key=True, index=True)
    quotation_number = Column(String(50), unique=True, index=True, nullable=False)
    quotation_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    valid_till = Column(DateTime, nullable=True)
    status = Column(Enum(QuotationStatus), default=QuotationStatus.DRAFT, nullable=False)
    
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    contact_person_id = Column(Integer, ForeignKey("contactperson.id"), nullable=True)
    sales_person_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    inquiry_reference = Column(String(255), nullable=True)
    billing_address = Column(Text, nullable=True)
    
    subtotal = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    shipping_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    grand_total = Column(Float, default=0.0)
    
    # terms_conditions = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", backref="quotations")
    contact_person = relationship("ContactPerson", backref="quotations")
    sales_person = relationship("User", backref="quotations")
    line_items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete-orphan")


class QuotationItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotation.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True)
    
    description = Column(Text, nullable=False)
    quantity = Column(Float, default=1.0)
    unit_price = Column(Float, default=0.0)
    tax_rate = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    
    quotation = relationship("Quotation", back_populates="line_items")
    product = relationship("Product")
