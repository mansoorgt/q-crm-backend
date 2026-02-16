from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import invoice as crud_invoice
from app.schemas.invoice import Invoice, InvoiceCreate, InvoiceUpdate, InvoicePagination

router = APIRouter()

@router.get("/", response_model=InvoicePagination)
def read_invoices(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = ""
) -> Any:
    invoices = crud_invoice.invoice.get_invoices(db, skip=skip, limit=limit, search=search)
    count = crud_invoice.invoice.count_invoices(db, search=search)
    return {"items": invoices, "total": count}

@router.post("/from-quotation/{quotation_id}", response_model=Invoice)
def create_invoice_from_quotation(
    *,
    db: Session = Depends(deps.get_db),
    quotation_id: int,
) -> Any:
    try:
        invoice = crud_invoice.invoice.create_from_quotation(db=db, quotation_id=quotation_id)
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{id}", response_model=Invoice)
def read_invoice(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    invoice = crud_invoice.invoice.get(db=db, id=id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/{id}", response_model=Invoice)
def update_invoice(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    invoice_in: InvoiceUpdate,
) -> Any:
    invoice = crud_invoice.invoice.get(db=db, id=id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice = crud_invoice.invoice.update(db=db, db_obj=invoice, obj_in=invoice_in)
    return invoice
