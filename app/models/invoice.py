from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.base_class import Base

class InvoiceStatus(str, enum.Enum):
    DRAFT = "Draft"
    SENT = "Sent"
    PAID = "Paid"
    OVERDUE = "Overdue"
    VOID = "Void"

class Invoice(Base):
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, index=True, nullable=False)
    invoice_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=True)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, nullable=False)
    
    quotation_id = Column(Integer, ForeignKey("quotation.id"), nullable=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    
    subtotal = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    shipping_amount = Column(Float, default=0.0)
    bank_charges = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    grand_total = Column(Float, default=0.0)
    
    amount_paid = Column(Float, default=0.0)
    balance_due = Column(Float, default=0.0)
    
    notes = Column(Text, nullable=True)
    # terms_conditions = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", backref="invoices")
    quotation = relationship("Quotation", backref="invoices")
    line_items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoice.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True)
    
    description = Column(Text, nullable=False)
    stock_availability = Column(String(50), nullable=True)
    quantity = Column(Float, default=1.0)
    unit_price = Column(Float, default=0.0)
    tax_rate = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    
    invoice = relationship("Invoice", back_populates="line_items")
    product = relationship("Product")
