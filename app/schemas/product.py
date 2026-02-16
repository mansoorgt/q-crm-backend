from typing import Optional, List
from pydantic import BaseModel

# Shared properties
class ProductStatusBase(BaseModel):
    name: Optional[str] = None
    key: Optional[str] = None

class CategoryBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProductBase(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = 0.0
    description: Optional[str] = None
    status_id: Optional[int] = None
    category_id: Optional[int] = None

# Properties to receive on creations
class ProductStatusCreate(ProductStatusBase):
    name: str
    key: str

class CategoryCreate(CategoryBase):
    name: str

class ProductCreate(ProductBase):
    name: str
    sku: str
    price: float
    status_id: int
    category_id: int

# Properties to receive on updates
class ProductStatusUpdate(ProductStatusBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class ProductUpdate(ProductBase):
    pass

# Properties shared by models stored in DB
class ProductStatusInDBBase(ProductStatusBase):
    id: int

    class Config:
        orm_mode = True

class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class ProductInDBBase(ProductBase):
    id: int

    class Config:
        orm_mode = True

# Properties to return to client
class ProductStatus(ProductStatusInDBBase):
    pass

class Category(CategoryInDBBase):
    pass

class Product(ProductInDBBase):
    status: Optional[ProductStatus] = None
    category: Optional[Category] = None

class ProductPagination(BaseModel):
    items: List[Product]
    total: int
