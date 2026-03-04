from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.models.invoice import InvoiceStatus
from app.schemas.customer import Customer
from app.schemas.quotation import ProductSimple

# --- Item Schemas ---
class InvoiceItemBase(BaseModel):
    product_id: Optional[int] = None
    description: str
    stock_availability: Optional[str] = None
    quantity: float = 1.0
    unit_price: float = 0.0
    tax_rate: float = 0.0
    total: float = 0.0

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItem(InvoiceItemBase):
    id: int
    invoice_id: int
    product: Optional[ProductSimple] = None

    class Config:
        from_attributes = True

# --- Invoice Schemas ---
class InvoiceBase(BaseModel):
    invoice_number: str
    invoice_date: datetime
    due_date: Optional[datetime] = None
    status: InvoiceStatus = InvoiceStatus.DRAFT
    
    customer_id: int
    quotation_id: Optional[int] = None
    
    subtotal: float
    discount_amount: float
    shipping_amount: float
    bank_charges: float = 0.0
    tax_amount: float
    grand_total: float
    
    amount_paid: float = 0.0
    balance_due: float = 0.0
    
    notes: Optional[str] = None
    # terms_conditions: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    line_items: List[InvoiceItemCreate]

class InvoiceUpdate(BaseModel):
    invoice_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    status: Optional[InvoiceStatus] = None
    
    subtotal: Optional[float] = None
    discount_amount: Optional[float] = None
    shipping_amount: Optional[float] = None
    bank_charges: Optional[float] = None
    tax_amount: Optional[float] = None
    grand_total: Optional[float] = None
    
    amount_paid: Optional[float] = None
    balance_due: Optional[float] = None
    
    notes: Optional[str] = None
    # terms_conditions: Optional[str] = None
    
    line_items: Optional[List[InvoiceItemCreate]] = None

class Invoice(InvoiceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    line_items: List[InvoiceItem] = []
    customer: Optional[Customer] = None

    class Config:
        from_attributes = True

class InvoicePagination(BaseModel):
    items: List[Invoice]
    total: int
