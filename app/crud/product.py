from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.product import Product, Category, ProductStatus
from app.schemas.product import ProductCreate, ProductUpdate, CategoryCreate, CategoryUpdate, ProductStatusCreate, ProductStatusUpdate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, search: Optional[str] = None
    ) -> List[Product]:
        query = db.query(self.model)
        if search:
             query = query.filter(self.model.name.ilike(f"%{search}%"))
        return query.offset(skip).limit(limit).all()

class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass

class CRUDProductStatus(CRUDBase[ProductStatus, ProductStatusCreate, ProductStatusUpdate]):
    def get_by_key(self, db: Session, *, key: str) -> Optional[ProductStatus]:
        return db.query(ProductStatus).filter(ProductStatus.key == key).first()

product = CRUDProduct(Product)
category = CRUDCategory(Category)
product_status = CRUDProductStatus(ProductStatus)
