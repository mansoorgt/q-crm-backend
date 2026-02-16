from typing import Optional

from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_approved: Optional[bool] = False
    is_superuser: bool = False
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    position_id: Optional[int] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
from .position import Position
class User(UserInDBBase):
    position: Optional[Position] = None

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
