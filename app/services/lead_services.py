from sqlalchemy.orm import Session
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCreate, LeadUpdate

class LeadService:
    def __init__(self, db: Session):
        self.repo = LeadRepository(db)

    def list_leads(self, filter: dict = None, page: int = 1, page_size: int = 10):
        return self.repo.GET_ALL(filter=filter, page=page, page_size=page_size)

    def get_lead(self, lead_id: int):
        lead = self.repo.GET_BY_ID(lead_id)
        if not lead:
            raise ValueError("Lead not found")
        return lead

    def create_lead(self, data: LeadCreate):
        return self.repo.CREATE(data)

    def update_lead(self, lead_id: int, data: LeadUpdate):
        lead = self.get_lead(lead_id)
        return self.repo.UPDATE(lead, data)

    def delete_lead(self, lead_id: int):
        lead = self.get_lead(lead_id)
        self.repo.DELETE(lead)
