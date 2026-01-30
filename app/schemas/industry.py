from datetime import datetime
from pydantic import BaseModel

class IndustryBase(BaseModel):
    name: str

class IndustryCreate(IndustryBase):
    pass

class IndustryUpdate(IndustryBase):
    pass

class IndustryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
