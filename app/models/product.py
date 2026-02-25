from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class ProductStatus(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    key = Column(String(255), unique=True, index=True, nullable=False)  # constant key for code reference
    
    products = relationship("Product", back_populates="status")

class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    products = relationship("Product", back_populates="category")

class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    sku = Column(String(255), unique=True, index=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    description = Column(Text, nullable=True)
    
    status_id = Column(Integer, ForeignKey("productstatus.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    
    status = relationship("ProductStatus", back_populates="products")
    category = relationship("Category", back_populates="products")
