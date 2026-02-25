from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate

class CRUDSupplier(CRUDBase[Supplier, SupplierCreate, SupplierUpdate]):
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, search: Optional[str] = None
    ) -> List[Supplier]:
        query = db.query(self.model)
        if search:
            query = query.filter(self.model.name.ilike(f"%{search}%"))
        return query.offset(skip).limit(limit).all()

supplier = CRUDSupplier(Supplier)
