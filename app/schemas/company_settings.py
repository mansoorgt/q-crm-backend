from typing import Optional
from pydantic import BaseModel

class CompanySettingsBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    trn: Optional[str] = None
    bank_details: Optional[str] = None
    logo_url: Optional[str] = None
    full_logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    quotation_terms_conditions: Optional[str] = None
    invoice_terms_conditions: Optional[str] = None

class CompanySettingsCreate(CompanySettingsBase):
    pass

class CompanySettingsUpdate(CompanySettingsBase):
    pass

class CompanySettings(CompanySettingsBase):
    id: int

    class Config:
        from_attributes = True
