from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.customer import Customer
from app.schemas.product import Product
from app.schemas.user import User

# Shared properties
class InquiryBase(BaseModel):
    customer_id: int
    contact_person_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = 1
    notes: Optional[str] = None
    source: Optional[str] = None
    assigned_to: Optional[int] = None
    status: Optional[str] = "New"

# Properties to receive on creation
class InquiryCreate(InquiryBase):
    pass

# Properties to receive on update
class InquiryUpdate(InquiryBase):
    customer_id: Optional[int] = None

# Properties shared by models stored in DB
class InquiryInDBBase(InquiryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return to client
class Inquiry(InquiryInDBBase):
    customer: Optional[Customer] = None
    product: Optional[Product] = None
    assignee: Optional[User] = None

class InquiryPagination(BaseModel):
    items: list[Inquiry]
    total: int
