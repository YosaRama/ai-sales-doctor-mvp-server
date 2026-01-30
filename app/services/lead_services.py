from sqlalchemy.orm import Session
from app.repositories.lead_repository import LeadRepository
from app.schemas.lead import LeadCreate, LeadUpdate
from app.core.exception import AppException

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
        try:
            if industry_ids:
                industry_ids = [int(id) for id in industry_ids.split(",")]
        except Exception:
            raise AppException(message="Invalid industry IDs", status_code=400)

        try:
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
        except Exception as e:
            raise AppException(message=str(e), status_code=500)

    def get_lead(self, lead_id: int):
        lead = self.repo.GET_BY_ID(lead_id)
        if not lead:
            raise AppException(message="Lead not found", status_code=404)
        return lead

    def create_lead(self, data: LeadCreate):
        try:
            return self.repo.CREATE(data)
        except Exception as e:
            raise AppException(message=str(e), status_code=500)

    def update_lead(self, lead_id: int, data: LeadUpdate):
        lead = self.get_lead(lead_id)
        return self.repo.UPDATE(lead, data)

    def delete_lead(self, lead_id: int):
        lead = self.get_lead(lead_id)
        self.repo.DELETE(lead)
