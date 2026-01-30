from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.repositories.industry_repository import IndustryRepository
from app.schemas.industry import IndustryCreate, IndustryUpdate
from app.core.exception import AppException

class IndustryService:
    def __init__(self, db: Session):
        self.repo = IndustryRepository(db)

    def list_industries(self):
        return self.repo.GET_ALL()

    def get_industry(self, industry_id: int):
        industry = self.repo.GET_BY_ID(industry_id)
        if not industry:
            raise AppException(message="Industry not found", status_code=404)
        return industry

    def create_industry(self, data: IndustryCreate):
        try:
            industry_data = data.model_dump()
            now = datetime.now(timezone.utc)
            industry_data["created_at"] = now
            industry_data["updated_at"] = now
            return self.repo.CREATE(industry_data)
        except Exception as e:
            raise AppException(message=str(e), status_code=500)

    def update_industry(self, industry_id: int, data: IndustryUpdate):
        try:
            industry = self.get_industry(industry_id)
            industry_data = data.model_dump()
            industry_data["updated_at"] = datetime.now()
            return self.repo.UPDATE(industry, industry_data)
        except Exception as e:
            raise AppException(message=str(e), status_code=500)

    def delete_industry(self, industry_id: int):
        try:
            industry = self.get_industry(industry_id)
            return self.repo.DELETE(industry)
        except Exception as e:
            raise AppException(message=str(e), status_code=500)
