
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse
from app.schemas.base import PaginatedResponse
from app.services.lead_services import LeadService

router = APIRouter(prefix="/api/v1/leads", tags=["Leads"])

@router.get("/", response_model=PaginatedResponse[LeadResponse])
def get_leads(
    db: Session = Depends(get_db),
    logic: str = Query("AND", regex="^(AND|OR)$"),
    page: int = 1,
    page_size: int = 10,
    name: str | None = None,
    headcount: str | None = None,
    industry_ids: str | None = None
):
    return LeadService(db).list_leads(
        logic=logic, 
        page=page, 
        page_size=page_size,
        name=name,
        headcount=headcount,
        industry_ids=industry_ids
    )

@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    try:
        return LeadService(db).get_lead(lead_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=LeadResponse)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    return LeadService(db).create_lead(payload)

@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: int, payload: LeadUpdate, db: Session = Depends(get_db)):
    try:
        return LeadService(db).update_lead(lead_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    try:
        LeadService(db).delete_lead(lead_id)
        return {"message": "Lead deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
