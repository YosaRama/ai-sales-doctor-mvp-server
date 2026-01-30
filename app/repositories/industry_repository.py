from sqlalchemy.orm import Session
from app.models.industry import Industry

class IndustryRepository:
    def __init__(self, db: Session):
        self.db = db

    def GET_ALL(self):
        return self.db.query(Industry).order_by(Industry.created_at.desc()).all()

    def GET_BY_ID(self, industry_id: int):
        return self.db.query(Industry).filter(Industry.id == industry_id).first()

    def CREATE(self, data: dict):
        industry = Industry(**data)
        self.db.add(industry)
        self.db.commit()
        self.db.refresh(industry)
        return industry
        
    def UPDATE(self, industry: Industry, data: dict):
        for field, value in data.items():
            setattr(industry, field, value)
        self.db.commit()
        self.db.refresh(industry)
        return industry
        
    def DELETE(self, industry: Industry):
        self.db.delete(industry)
        self.db.commit()
        return True