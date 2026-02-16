from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=schemas.inquiry.InquiryPagination)
def read_inquiries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve inquiries.
    """
    total = db.query(models.Inquiry).count()
    inquiries = crud.inquiry.get_multi(db, skip=skip, limit=limit)
    return {"items": inquiries, "total": total}

@router.get("/{id}", response_model=schemas.inquiry.Inquiry)
def read_inquiry(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get inquiry by ID.
    """
    inquiry = crud.inquiry.get(db=db, id=id)
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry

@router.post("/", response_model=schemas.inquiry.Inquiry)
def create_inquiry(
    *,
    db: Session = Depends(deps.get_db),
    inquiry_in: schemas.inquiry.InquiryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new inquiry.
    """
    inquiry = crud.inquiry.create(db=db, obj_in=inquiry_in)
    return inquiry

@router.put("/{id}", response_model=schemas.inquiry.Inquiry)
def update_inquiry(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    inquiry_in: schemas.inquiry.InquiryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an inquiry.
    """

    inquiry = crud.inquiry.get(db=db, id=id)
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    inquiry = crud.inquiry.update(db=db, db_obj=inquiry, obj_in=inquiry_in)
    return inquiry

@router.delete("/{id}", response_model=schemas.inquiry.Inquiry)
def delete_inquiry(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an inquiry.
    """
    inquiry = crud.inquiry.get(db=db, id=id)
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    inquiry = crud.inquiry.remove(db=db, id=id)
    return inquiry
