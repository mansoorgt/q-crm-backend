from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class CompanySettings(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    trn = Column(String(50), nullable=True)
    bank_details = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    full_logo_url = Column(String(500), nullable=True)
    primary_color = Column(String(50), nullable=True)
    secondary_color = Column(String(50), nullable=True)
    quotation_terms_conditions = Column(Text, nullable=True)
    invoice_terms_conditions = Column(Text, nullable=True)
