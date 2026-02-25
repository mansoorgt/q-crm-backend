from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Supplier(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    email = Column(String(255), index=True, nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
