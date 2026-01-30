from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate
from sqlalchemy import or_, and_


class LeadRepository:
    def __init__(self, db: Session):
        self.db = db

    def GET_ALL(
        self,
        page: int = 1,
        page_size: int = 10,
        name: str | None = None,
        headcount: str | None = None,
        industry_ids: list[int] | None = None,
        logic: str = "AND",
    ):
        offset = (page - 1) * page_size
        query = self.db.query(Lead)

        conditions = []

        if name:
            conditions.append(Lead.name.ilike(f"%{name}%"))

        if headcount:
            if "-" in headcount:
                min_val, max_val = map(int, headcount.split("-"))
                conditions.append(Lead.headcount.between(min_val, max_val))
            else:
                conditions.append(Lead.headcount == int(headcount))

        if industry_ids:
            conditions.append(Lead.industry_id.in_(industry_ids))

        if conditions:
            query = query.filter(
                or_(*conditions) if logic == "OR" else and_(*conditions)
            )

        total = query.count()

        items = (
            query.order_by(Lead.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return {
            "result": items,
            "total": total,
        }


    def GET_BY_ID(self, lead_id: int):
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def CREATE(self, data: LeadCreate):
        lead = Lead(**data.model_dump())

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
