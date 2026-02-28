from typing import Optional, List
from pydantic import BaseModel
from .permission import Permission

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []

class RoleUpdate(RoleBase):
    name: Optional[str] = None
    permission_ids: Optional[List[int]] = None

class RoleInDBBase(RoleBase):
    id: int
    permissions: List[Permission] = []

    class Config:
        from_attributes = True

class Role(RoleInDBBase):
    pass

class RoleInDB(RoleInDBBase):
    pass
