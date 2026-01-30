from sqlalchemy.orm import Session, joinedload
from app.core.exception import AppException
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
        order_by: str | None = "updated_at",
        order_dir: str = "DESC",
    ):
        try:
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

            if order_by:
                if order_dir.upper() == "ASC":
                    query = query.order_by(getattr(Lead, order_by).asc())
                else:
                    query = query.order_by(getattr(Lead, order_by).desc())

            items = (
                query.offset(offset)
                .limit(page_size)
                .options(
                    joinedload(Lead.industry),
                )
                .all()
            )


            return {
                "result": items,
                "total": total,
            }
        except Exception as e:
            print(f"Error in list_leads: {e}")
            raise AppException(message=str(e), status_code=500)


    def GET_BY_ID(self, lead_id: int):
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def CREATE(self, data: dict):
        try:
            lead = Lead(**data)

            existing_lead = self.db.query(Lead).filter(Lead.email == lead.email).first()
            if existing_lead:
                raise AppException(message="Lead with email already exists", status_code=400)

            if lead.industry_id is not None:
                from app.models.industry import Industry
                industry = self.db.query(Industry).filter(Industry.id == lead.industry_id).first()
                if not industry:
                    raise AppException(message="Industry not found", status_code=404)
            
            self.db.add(lead)
            self.db.commit()
            self.db.refresh(lead)
            return lead
        except Exception as e:
            raise AppException(message=str(e), status_code=500)

    def UPDATE(self, lead: Lead, data: LeadUpdate):
        for field, value in data.model_dump().items():
            setattr(lead, field, value)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def DELETE(self, lead: Lead):
        self.db.delete(lead)
        self.db.commit()
