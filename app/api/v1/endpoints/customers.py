from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=schemas.customer.CustomerPagination)
def read_customers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve customers.
    """
    if search:
         total = db.query(models.Customer).filter(models.Customer.name.ilike(f"%{search}%")).count()
         customers = crud.customer.get_multi(db, skip=skip, limit=limit, search=search)
    else:
        total = db.query(models.Customer).count()
        customers = crud.customer.get_multi(db, skip=skip, limit=limit)
        
    return {"items": customers, "total": total}

@router.post("/", response_model=schemas.customer.Customer)
def create_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_in: schemas.customer.CustomerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new customer with contact persons.
    """
    customer = crud.customer.create_with_contact_persons(db=db, obj_in=customer_in)
    return customer

@router.put("/{id}", response_model=schemas.customer.Customer)
def update_customer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    customer_in: schemas.customer.CustomerUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a customer.
    """
    customer = crud.customer.get(db=db, id=id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer = crud.customer.update_with_contact_persons(db=db, db_obj=customer, obj_in=customer_in)
    return customer

@router.delete("/{id}", response_model=schemas.customer.Customer)
def delete_customer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a customer.
    """
    customer = crud.customer.get(db=db, id=id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer = crud.customer.remove(db=db, id=id)
    return customer
