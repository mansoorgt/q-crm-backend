from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate
from app.crud.permission import permission as crud_permission

class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()
        
    def create(self, db: Session, *, obj_in: RoleCreate) -> Role:
        db_obj = Role(
            name=obj_in.name,
            description=obj_in.description,
        )
        if obj_in.permission_ids:
            permissions = crud_permission.get_multi_by_ids(db, ids=obj_in.permission_ids)
            db_obj.permissions = permissions
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Role, obj_in: RoleUpdate) -> Role:
        update_data = obj_in.dict(exclude_unset=True)
        if "permission_ids" in update_data:
            permission_ids = update_data.pop("permission_ids")
            permissions = crud_permission.get_multi_by_ids(db, ids=permission_ids)
            db_obj.permissions = permissions
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

role = CRUDRole(Role)
