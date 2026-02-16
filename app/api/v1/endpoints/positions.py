from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Position])
def read_positions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve positions.
    """
    positions = crud.position.get_multi(db, skip=skip, limit=limit)
    return positions

@router.post("/", response_model=schemas.Position)
def create_position(
    *,
    db: Session = Depends(deps.get_db),
    position_in: schemas.PositionCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new position.
    """
    position = crud.position.create(db, obj_in=position_in)
    return position
