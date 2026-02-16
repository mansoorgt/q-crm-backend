from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

# class InquiryStatus(str, enum.Enum):
#     NEW = "NEW"
#     CONTACTED = "CONTACTED"
#     QUALIFIED = "QUALIFIED"
#     PROPOSAL_SENT = "PROPOSAL_SENT"
#     CONVERTED = "CONVERTED"
#     LOST = "LOST"
#     WON = "WON"

class Inquiry(Base):
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    contact_person_id = Column(Integer, ForeignKey("contactperson.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=True)
    quantity = Column(Integer, default=1)
    notes = Column(Text, nullable=True)
    source = Column(String(255), nullable=True)
    assigned_to = Column(Integer, ForeignKey("user.id"), nullable=True)
    status = Column(String(50), default="New")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer")
    contact_person = relationship("ContactPerson")
    product = relationship("Product")
    assignee = relationship("User")
