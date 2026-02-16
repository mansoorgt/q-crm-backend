from typing import Optional

from pydantic import BaseModel

# Shared properties
class PositionBase(BaseModel):
    name: Optional[str] = None

# Properties to receive via API on creation
class PositionCreate(PositionBase):
    name: str

# Properties to receive via API on update
class PositionUpdate(PositionBase):
    pass

class PositionInDBBase(PositionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class Position(PositionInDBBase):
    pass
