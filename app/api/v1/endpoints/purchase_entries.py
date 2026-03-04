from typing import Any
import shutil
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import purchase_entry as crud_purchase_entry
from app.schemas.purchase_entry import PurchaseEntry, PurchaseEntryCreate, PurchaseEntryUpdate, PurchaseEntryPagination, PurchaseEntryAttachmentBase
from app.models.purchase_entry import PurchaseEntryAttachment
from app.models.user import User

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

@router.post("/{id}/attachments", response_model=PurchaseEntryAttachmentBase)
async def upload_purchase_attachment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Ensure entry exists
    entry = crud_purchase_entry.get_purchase_entry(db=db, purchase_id=id)
    if not entry:
        raise HTTPException(status_code=404, detail="Purchase entry not found")

    file_location = f"{UPLOAD_DIR}/purchase_{id}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    file_url = f"/static/purchase_{id}_{file.filename}"
    
    attachment = PurchaseEntryAttachment(
        purchase_entry_id=id,
        file_name=file.filename,
        file_url=file_url
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    
    return attachment

@router.delete("/{id}/attachments/{attachment_id}")
def delete_purchase_attachment(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    attachment_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    attachment = db.query(PurchaseEntryAttachment).filter(
        PurchaseEntryAttachment.id == attachment_id,
        PurchaseEntryAttachment.purchase_entry_id == id
    ).first()
    
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
        
    # Attempt to remove file
    file_path = attachment.file_url.replace("/static/", f"{UPLOAD_DIR}/")
    if os.path.exists(file_path):
        os.remove(file_path)
        
    db.delete(attachment)
    db.commit()
    return {"success": True}
