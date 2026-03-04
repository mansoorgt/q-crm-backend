from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .supplier import Supplier
from .product import Product

class InvoiceSimple(BaseModel):
    id: int
    invoice_number: str

    class Config:
        from_attributes = True

class PurchaseEntryAttachmentBase(BaseModel):
    id: int
    purchase_entry_id: int
    file_name: str
    file_url: str
    created_at: datetime

    class Config:
        from_attributes = True

class PurchaseEntryItemBase(BaseModel):
    product_id: Optional[int] = None
    quantity: float
    price: float = 0.0
    amount: float = 0.0

class PurchaseEntryItemCreate(PurchaseEntryItemBase):
    pass

class PurchaseEntryItemUpdate(PurchaseEntryItemBase):
    pass

class PurchaseEntryItem(PurchaseEntryItemBase):
    id: int
    purchase_entry_id: int
    product: Optional[Product] = None

    class Config:
        from_attributes = True

class PurchaseEntryBase(BaseModel):
    purchase_date: datetime
    supplier_id: int
    subtotal: float = 0.0
    grand_total: float = 0.0
    created_by_id: Optional[int] = None
    invoice_id: Optional[int] = None

class PurchaseEntryCreate(PurchaseEntryBase):
    line_items: List[PurchaseEntryItemCreate]
    purchase_number: Optional[str] = None

class PurchaseEntryUpdate(PurchaseEntryBase):
    line_items: List[PurchaseEntryItemCreate]

class PurchaseEntry(PurchaseEntryBase):
    id: int
    purchase_number: str
    created_at: datetime
    updated_at: datetime
    line_items: List[PurchaseEntryItem]
    
    # Nested objects
    supplier: Optional[Supplier] = None
    invoice: Optional[InvoiceSimple] = None
    attachments: List[PurchaseEntryAttachmentBase] = []

    class Config:
        from_attributes = True

class PurchaseEntryPagination(BaseModel):
    items: List[PurchaseEntry]
    total: int
