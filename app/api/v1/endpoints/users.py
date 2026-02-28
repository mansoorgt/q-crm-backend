from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser), # Remove dependency if public registration wanted
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    email: EmailStr = Body(...),
    password: str = Body(...),
    full_name: str = Body(None),
    phone_number: str = Body(None),
    address: str = Body(None),
    position_id: int = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(
        password=password, 
        email=email, 
        full_name=full_name, 
        phone_number=phone_number, 
        address=address, 
        position_id=position_id
    )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a user. Only superusers or someone with settings_access.
    """
    has_settings_access = False
    if current_user.role:
        has_settings_access = any(p.name == "settings_access" for p in current_user.role.permissions)

    if not current_user.is_superuser and not has_settings_access:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user_in.email:
        existing_user = crud.user.get_by_email(db, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system",
            )
        
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.post("/{user_id}/approve", response_model=schemas.User)
def approve_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Approve a newly registered user.
    """
    has_settings_access = False
    if current_user.role:
        has_settings_access = any(p.name == "settings_access" for p in current_user.role.permissions)

    if not current_user.is_superuser and not has_settings_access:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user = crud.user.update(db, db_obj=user, obj_in={"is_approved": True})
    return user

@router.post("/{user_id}/deactivate", response_model=schemas.User)
def deactivate_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Deactivate a user.
    """
    has_settings_access = False
    if current_user.role:
        has_settings_access = any(p.name == "settings_access" for p in current_user.role.permissions)

    if not current_user.is_superuser and not has_settings_access:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user = crud.user.update(db, db_obj=user, obj_in={"is_active": False})
    return user


@router.post("/{user_id}/activate", response_model=schemas.User)
def activate_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Activate a deactivated user.
    """
    has_settings_access = False
    if current_user.role:
        has_settings_access = any(p.name == "settings_access" for p in current_user.role.permissions)

    if not current_user.is_superuser and not has_settings_access:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user = crud.user.update(db, db_obj=user, obj_in={"is_active": True})
    return user
