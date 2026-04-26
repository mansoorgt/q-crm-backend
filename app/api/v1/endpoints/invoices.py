from typing import Any, List
import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body, Response
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader
import weasyprint

from app.api import deps
from app.crud import invoice as crud_invoice
from app.models.company_settings import CompanySettings
from app.schemas.invoice import Invoice, InvoiceCreate, InvoiceUpdate, InvoicePagination, InvoicePayment, InvoicePaymentCreate

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

@router.post("/", response_model=Invoice)
def create_invoice(
    *,
    db: Session = Depends(deps.get_db),
    invoice_in: InvoiceCreate,
) -> Any:
    """
    Create new invoice.
    """
    if invoice_in.invoice_number in ["LOADING...", "Will be generated"] or not invoice_in.invoice_number:
        invoice_in.invoice_number = crud_invoice.invoice.get_next_invoice_number(db)
        
    invoice = crud_invoice.invoice.create_with_items(db=db, obj_in=invoice_in)
    return invoice

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
        error_msg = str(e)
        if error_msg.startswith("Invoice already exists for this quotation:"):
            existing_id = int(error_msg.split(":")[1])
            raise HTTPException(
                status_code=400, 
                detail={"message": "Invoice already exists for this quotation", "invoice_id": existing_id}
            )
        raise HTTPException(status_code=404, detail=error_msg)

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

@router.post("/{id}/payments", response_model=InvoicePayment)
def add_payment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    payment_in: InvoicePaymentCreate,
) -> Any:
    try:
        payment = crud_invoice.invoice.add_payment(db=db, invoice_id=id, payment_in=payment_in)
        return payment
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id}/payments/{payment_id}")
def delete_payment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    payment_id: int,
) -> Any:
    try:
        success = crud_invoice.invoice.delete_payment(db=db, invoice_id=id, payment_id=payment_id)
        return {"success": success}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{id}/pdf")
def generate_invoice_pdf(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    invoice = crud_invoice.invoice.get(db=db, id=id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    settings = db.query(CompanySettings).first()
    
    template_dir = os.path.join(os.path.dirname(__file__), "../../../templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("invoice.html")
    
    # Format dates
    date_str = invoice.invoice_date.strftime("%b %d, %Y") if invoice.invoice_date else ""
    due_date_str = invoice.due_date.strftime("%b %d, %Y") if invoice.due_date else ""
    
    # Resolve logo URL
    logo_url = ""
    if settings:
        if settings.full_logo_url:
            logo_url = settings.full_logo_url
        elif settings.logo_url:
            logo_url = settings.logo_url
            
        # Weasyprint needs absolute local paths or complete URLs. 
        # If it's a relative /static/ path, map it to the uploads folder
        if logo_url.startswith("/static/"):
            # assuming uploads is at the root of backend
            logo_path = os.path.join(os.getcwd(), "uploads", logo_url.replace("/static/", ""))
            if os.path.exists(logo_path):
                logo_url = "file://" + logo_path
    
    html_out = template.render(
        invoice=invoice,
        settings=settings,
        date_str=date_str,
        due_date_str=due_date_str,
        logo_url=logo_url
    )
    
    # Generate PDF
    pdf_bytes = weasyprint.HTML(string=html_out, base_url="").write_pdf()
    
    return Response(content=pdf_bytes, media_type="application/pdf")
