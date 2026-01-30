from pydantic import BaseModel, EmailStr

class IndustryBase(BaseModel):
    name: str
    created_at: str
    updated_at: str

class IndustryCreate(IndustryBase):
    pass

class IndustryUpdate(IndustryBase):
    pass

class IndustryResponse(BaseModel):
    id: int
    name: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
