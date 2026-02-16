from sqlalchemy import Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    type = Column(String(50), nullable=False) # 'individual' or 'company'
    email = Column(String(255), index=True, nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    
    contact_persons = relationship("ContactPerson", back_populates="customer", cascade="all, delete-orphan")

class ContactPerson(Base):
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    role = Column(String(100), nullable=True)
    
    customer = relationship("Customer", back_populates="contact_persons")
