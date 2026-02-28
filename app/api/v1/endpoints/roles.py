from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Role])
def read_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve roles.
    """
    # Anyone who is active can retrieve roles for dropdowns, etc. Or you can restrict it.
    roles = crud.role.get_multi(db, skip=skip, limit=limit)
    return roles

@router.post("/", response_model=schemas.Role)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: schemas.RoleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new role. Only superuser or someone with settings_access.
    """
    has_settings_access = False
    if current_user.role:
        has_settings_access = any(p.name == "settings_access" for p in current_user.role.permissions)

    if not current_user.is_superuser and not has_settings_access:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    role = crud.role.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="A role with this name already exists.",
        )
    role = crud.role.create(db, obj_in=role_in)
    return role

@router.put("/{role_id}", response_model=schemas.Role)
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    role_in: schemas.RoleUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a role.
    """
    has_settings_access = False
    if current_user.role:
        has_settings_access = any(p.name == "settings_access" for p in current_user.role.permissions)

    if not current_user.is_superuser and not has_settings_access:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    role = crud.role.update(db, db_obj=role, obj_in=role_in)
    return role

@router.get("/{role_id}", response_model=schemas.Role)
def read_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get role by ID.
    """
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/{role_id}", response_model=schemas.Role)
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a role.
    """
    has_settings_access = False
    if current_user.role:
        has_settings_access = any(p.name == "settings_access" for p in current_user.role.permissions)

    if not current_user.is_superuser and not has_settings_access:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    role = crud.role.remove(db, id=role_id)
    return role
