from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=schemas.supplier.SupplierPagination)
def read_suppliers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve suppliers.
    """
    if search:
         total = db.query(models.Supplier).filter(models.Supplier.name.ilike(f"%{search}%")).count()
         suppliers = crud.supplier.get_multi(db, skip=skip, limit=limit, search=search)
    else:
        total = db.query(models.Supplier).count()
        suppliers = crud.supplier.get_multi(db, skip=skip, limit=limit)
        
    return {"items": suppliers, "total": total}

@router.post("/", response_model=schemas.supplier.Supplier)
def create_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_in: schemas.supplier.SupplierCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new supplier.
    """
    supplier = crud.supplier.create(db=db, obj_in=supplier_in)
    return supplier

@router.put("/{id}", response_model=schemas.supplier.Supplier)
def update_supplier(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    supplier_in: schemas.supplier.SupplierUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a supplier.
    """
    supplier = crud.supplier.get(db=db, id=id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier = crud.supplier.update(db=db, db_obj=supplier, obj_in=supplier_in)
    return supplier

@router.delete("/{id}", response_model=schemas.supplier.Supplier)
def delete_supplier(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a supplier.
    """
    supplier = crud.supplier.get(db=db, id=id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier = crud.supplier.remove(db=db, id=id)
    return supplier
