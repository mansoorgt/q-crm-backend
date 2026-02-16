from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Contact Person Schemas
class ContactPersonBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None

class ContactPersonCreate(ContactPersonBase):
    pass

class ContactPersonUpdate(ContactPersonBase):
    pass

class ContactPerson(ContactPersonBase):
    id: int
    customer_id: int

    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    type: str # 'individual' or 'company'
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    contact_persons: Optional[List[ContactPersonCreate]] = []

class CustomerUpdate(CustomerBase):
    contact_persons: Optional[List[ContactPersonCreate]] = []

class Customer(CustomerBase):
    id: int
    contact_persons: List[ContactPerson] = []

    class Config:
        from_attributes = True

class CustomerPagination(BaseModel):
    items: List[Customer]
    total: int
