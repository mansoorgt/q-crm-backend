from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import purchase_entry as crud_purchase_entry
from app.schemas.purchase_entry import PurchaseEntry, PurchaseEntryCreate, PurchaseEntryUpdate, PurchaseEntryPagination
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=PurchaseEntryPagination)
def read_purchase_entries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    entries = crud_purchase_entry.get_purchase_entries(db, skip=skip, limit=limit, search=search)
    count = crud_purchase_entry.count_purchase_entries(db, search=search)
    return {"items": entries, "total": count}

@router.get("/number", response_model=str)
def get_next_number(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return crud_purchase_entry.get_next_purchase_number(db)

@router.post("/", response_model=PurchaseEntry)
def create_purchase_entry(
    *,
    db: Session = Depends(deps.get_db),
    entry_in: PurchaseEntryCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    entry_in.created_by_id = current_user.id
    entry = crud_purchase_entry.create_purchase_entry(db=db, entry=entry_in)
    return entry

@router.get("/{id}", response_model=PurchaseEntry)
def read_purchase_entry(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    entry = crud_purchase_entry.get_purchase_entry(db=db, purchase_id=id)
    if not entry:
        raise HTTPException(status_code=404, detail="Purchase entry not found")
    return entry

@router.put("/{id}", response_model=PurchaseEntry)
def update_purchase_entry(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    entry_in: PurchaseEntryUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    entry = crud_purchase_entry.get_purchase_entry(db=db, purchase_id=id)
    if not entry:
        raise HTTPException(status_code=404, detail="Purchase entry not found")
    entry = crud_purchase_entry.update_purchase_entry(db=db, entry_id=id, entry_update=entry_in)
    return entry

@router.delete("/{id}")
def delete_purchase_entry(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    entry = crud_purchase_entry.get_purchase_entry(db=db, purchase_id=id)
    if not entry:
        raise HTTPException(status_code=404, detail="Purchase entry not found")
    entry = crud_purchase_entry.delete_purchase_entry(db=db, entry_id=id)
    return {"success": True}
