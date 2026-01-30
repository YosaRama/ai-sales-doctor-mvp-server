from sqlalchemy.orm import Session
from app.repositories.industry_repository import IndustryRepository
from app.schemas.industry import IndustryCreate, IndustryUpdate

class IndustryService:
    def __init__(self, db: Session):
        self.repo = IndustryRepository(db)

    def list_industries(self):
        return self.repo.GET_ALL()

    def get_industry(self, industry_id: int):
        industry = self.repo.GET_BY_ID(industry_id)
        if not industry:
            raise ValueError("Industry not found")
        return industry

    def create_industry(self, data: IndustryCreate):
        return self.repo.CREATE(data)

    def update_industry(self, industry_id: int, data: IndustryUpdate):
        industry = self.get_industry(industry_id)
        return self.repo.UPDATE(industry, data)

    def delete_industry(self, industry_id: int):
        industry = self.get_industry(industry_id)
        return self.repo.DELETE(industry)
