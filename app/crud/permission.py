from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate

class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.name == name).first()
    
    def get_multi_by_ids(self, db: Session, *, ids: List[int]) -> List[Permission]:
        return db.query(Permission).filter(Permission.id.in_(ids)).all()

permission = CRUDPermission(Permission)
