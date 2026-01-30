from datetime import datetime
from pydantic import BaseModel, EmailStr

class LeadBase(BaseModel):
    name: str
    job_title: str
    phone_number: str
    company: str
    email: EmailStr
    headcount: int
    industry_id: int

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
