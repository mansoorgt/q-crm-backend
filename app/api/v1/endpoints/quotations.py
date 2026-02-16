from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import quotation as crud_quotation
from app.schemas.quotation import Quotation, QuotationCreate, QuotationUpdate, QuotationPagination

router = APIRouter()

@router.get("/", response_model=QuotationPagination)
def read_quotations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = ""
) -> Any:
    quotations = crud_quotation.get_quotations(db, skip=skip, limit=limit, search=search)
    count = crud_quotation.count_quotations(db, search=search)
    return {"items": quotations, "total": count}

@router.get("/number", response_model=str)
def get_next_number(
    db: Session = Depends(deps.get_db),
) -> Any:
    return crud_quotation.get_next_quotation_number(db)

@router.post("/", response_model=Quotation)
def create_quotation(
    *,
    db: Session = Depends(deps.get_db),
    quotation_in: QuotationCreate,
) -> Any:
    print(quotation_in,'log-----')
    quotation = crud_quotation.create_quotation(db=db, quotation=quotation_in)
    return quotation

@router.get("/{id}", response_model=Quotation)
def read_quotation(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    quotation = crud_quotation.get_quotation(db=db, quotation_id=id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation

@router.put("/{id}", response_model=Quotation)
def update_quotation(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    quotation_in: QuotationUpdate,
) -> Any:
    quotation = crud_quotation.get_quotation(db=db, quotation_id=id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    quotation = crud_quotation.update_quotation(db=db, quotation_id=id, quotation_update=quotation_in)
    return quotation

@router.delete("/{id}", response_model=Quotation)
def delete_quotation(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    quotation = crud_quotation.get_quotation(db=db, quotation_id=id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    quotation = crud_quotation.delete_quotation(db=db, quotation_id=id)
    return quotation
