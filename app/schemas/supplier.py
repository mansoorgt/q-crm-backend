from typing import List, Optional
from pydantic import BaseModel, EmailStr

class SupplierBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True

class SupplierPagination(BaseModel):
    items: List[Supplier]
    total: int
