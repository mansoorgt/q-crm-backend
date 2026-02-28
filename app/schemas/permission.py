from typing import Optional
from pydantic import BaseModel

# Shared properties
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

# Properties to receive on creation
class PermissionCreate(PermissionBase):
    pass

# Properties to receive on update
class PermissionUpdate(PermissionBase):
    pass

# Properties shared by models stored in DB
class PermissionInDBBase(PermissionBase):
    id: int

    class Config:
        from_attributes = True

# Properties to return to client
class Permission(PermissionInDBBase):
    pass

# Properties stored in DB
class PermissionInDB(PermissionInDBBase):
    pass
