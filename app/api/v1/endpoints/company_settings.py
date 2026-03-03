from typing import Any
import shutil
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.models.company_settings import CompanySettings
from app.schemas.company_settings import CompanySettingsCreate, CompanySettingsUpdate, CompanySettings as CompanySettingsSchema

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=CompanySettingsSchema)
def get_company_settings(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get company settings.
    """
    settings = db.query(CompanySettings).first()
    if not settings:
        # Create default empty settings if none exist
        settings = CompanySettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("/", response_model=CompanySettingsSchema)
def update_company_settings(
    *,
    db: Session = Depends(deps.get_db),
    settings_in: CompanySettingsUpdate,
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update company settings. Only superusers.
    """
    settings = db.query(CompanySettings).first()
    if not settings:
        settings = CompanySettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    update_data = settings_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)

    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings

@router.post("/logo", response_model=CompanySettingsSchema)
async def upload_company_logo(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Upload company logo. Only superusers.
    """
    settings = db.query(CompanySettings).first()
    if not settings:
        settings = CompanySettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    # Assuming the server serves static files from /static
    # The URL should be relative or absolute depending on frontend needs.
    # We'll store the relative path for now.
    logo_url = f"/static/{file.filename}"
    
    settings.logo_url = logo_url
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings

@router.post("/full-logo", response_model=CompanySettingsSchema)
async def upload_company_full_logo(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Upload full company logo text. Only superusers.
    """
    settings = db.query(CompanySettings).first()
    if not settings:
        settings = CompanySettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    file_location = f"{UPLOAD_DIR}/full_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    # Store the relative path
    full_logo_url = f"/static/full_{file.filename}"
    
    settings.full_logo_url = full_logo_url
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings
