from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.models.position import Position
from app.schemas.position import PositionCreate, PositionUpdate

class CRUDPosition:
    def get(self, db: Session, id: Any) -> Optional[Position]:
        return db.query(Position).filter(Position.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Position]:
        return db.query(Position).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: PositionCreate) -> Position:
        db_obj = Position(name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Position:
        obj = db.query(Position).get(id)
        db.delete(obj)
        db.commit()
        return obj

position = CRUDPosition()
