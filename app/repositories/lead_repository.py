from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate

class LeadRepository:
    def __init__(self, db: Session):
        self.db = db

    def GET_ALL(self, page: int = 1, page_size: int = 10, filter: str = None):
        offset = (page - 1) * page_size
        query = self.db.query(Lead)
        total = query.count()

        # filter by name, industries, headcount by range
        if filter:
            filter_parts = filter.split(" ")
            for part in filter_parts:
                if ":" in part:
                    key, value = part.split(":")
                    if key == "name":
                        query = query.filter(Lead.name.contains(value))
                    elif key == "industry":
                        query = query.filter(Lead.industry.contains(value))
                    elif key == "headcount":
                        headcount_range = value.split("-")
                        if len(headcount_range) == 2:
                            headcount_min, headcount_max = headcount_range
                            query = query.filter(Lead.headcount.between(headcount_min, headcount_max))
                        elif len(headcount_range) == 1:
                            headcount_min = headcount_range[0]
                            query = query.filter(Lead.headcount >= headcount_min)
        
        items = (
            query
            .offset(offset)
            .limit(page_size)
            .order_by(Lead.created_at.desc())
            .all()
        )

        return {
            "result": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    def GET_BY_ID(self, lead_id: int):
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def CREATE(self, data: LeadCreate):
        lead = Lead(**data.model_dump())

        # add validation checking existing leads
        existing_lead = self.db.query(Lead).filter(Lead.email == data.email).first()
        if existing_lead:
            raise ValueError("Lead with email already exists")
        
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def UPDATE(self, lead: Lead, data: LeadUpdate):
        for field, value in data.model_dump().items():
            setattr(lead, field, value)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def DELETE(self, lead: Lead):
        self.db.delete(lead)
        self.db.commit()
