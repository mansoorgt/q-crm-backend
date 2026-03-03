from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.models.quotation import QuotationStatus
from app.schemas.customer import Customer, ContactPerson
from app.schemas.user import User as SalesPerson

# --- Product Schema Reference (Simplified) ---
class ProductSimple(BaseModel):
    id: int
    name: str
    sku: str
    
    class Config:
        from_attributes = True

# --- Item Schemas ---
class QuotationItemBase(BaseModel):
    product_id: Optional[int] = None
    description: str
    quantity: float = 1.0
    unit_price: float = 0.0
    tax_rate: float = 0.0
    total: float = 0.0

class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItemUpdate(QuotationItemBase):
    pass

class QuotationItem(QuotationItemBase):
    id: int
    quotation_id: int
    product: Optional[ProductSimple] = None

    class Config:
        from_attributes = True


# --- Quotation Schemas ---
class QuotationBase(BaseModel):
    quotation_number: str
    quotation_date: datetime
    valid_till: Optional[datetime] = None
    status: QuotationStatus = QuotationStatus.DRAFT
    
    customer_id: int
    contact_person_id: Optional[int] = None
    sales_person_id: Optional[int] = None
    inquiry_reference: Optional[str] = None
    billing_address: Optional[str] = None
    
    subtotal: float
    discount_amount: float
    shipping_amount: float
    tax_amount: float
    grand_total: float
    
    #terms_conditions: Optional[str] = None
    internal_notes: Optional[str] = None

class QuotationCreate(QuotationBase):
    line_items: List[QuotationItemCreate]

class QuotationUpdate(BaseModel): # Allowing partial updates
    quotation_number: Optional[str] = None
    quotation_date: Optional[datetime] = None
    valid_till: Optional[datetime] = None
    status: Optional[QuotationStatus] = None
    
    customer_id: Optional[int] = None
    contact_person_id: Optional[int] = None
    sales_person_id: Optional[int] = None
    billing_address: Optional[str] = None
    
    subtotal: Optional[float] = None
    discount_amount: Optional[float] = None
    shipping_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    grand_total: Optional[float] = None
    
    #terms_conditions: Optional[str] = None
    internal_notes: Optional[str] = None
    
    line_items: Optional[List[QuotationItemCreate]] = None

class Quotation(QuotationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    line_items: List[QuotationItem] = []
    customer: Optional[Customer] = None
    contact_person: Optional[ContactPerson] = None
    sales_person: Optional[SalesPerson] = None

    class Config:
        from_attributes = True

class QuotationPagination(BaseModel):
    items: List[Quotation]
    total: int

