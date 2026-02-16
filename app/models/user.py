from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_approved = Column(Boolean(), default=False)
    
    phone_number = Column(String(255), index=True, nullable=True)
    address = Column(String(255), nullable=True)
    position_id = Column(Integer, ForeignKey("position.id"), nullable=True)
    
    position = relationship("Position")
