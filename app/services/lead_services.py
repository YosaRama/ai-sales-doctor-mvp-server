from sqlalchemy.orm import Session
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse

class LeadService:
    def __init__(self, db: Session):
        self.repo = LeadRepository(db)

    def list_leads(
            self, 
            logic: str = "AND",  
            page: int = 1, 
            page_size: int = 10,
            name: str | None = None,
            headcount: str | None = None,
            industry_ids: str | None = None
        ):

        if industry_ids:
            industry_ids = [int(id) for id in industry_ids.split(",")]

        repo_result = self.repo.GET_ALL(
            page=page, 
            page_size=page_size,
            name=name,
            headcount=headcount,
            industry_ids=industry_ids,
            logic=logic, 
        )
        
        return {
            "result": repo_result["result"],
            "total": repo_result["total"],
        }

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
