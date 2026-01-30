from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.industry import IndustryCreate, IndustryUpdate, IndustryResponse
from app.services.industry_services import IndustryService

router = APIRouter(prefix="/industries", tags=["Industries"])

@router.get("/", response_model=list[IndustryResponse])
def get_industries(
    db: Session = Depends(get_db),
):
    return IndustryService(db).list_industries()

@router.get("/{industry_id}", response_model=IndustryResponse)
def get_industry(industry_id: int, db: Session = Depends(get_db)):
    try:
        return IndustryService(db).get_industry(industry_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=IndustryResponse)
def create_industry(payload: IndustryCreate, db: Session = Depends(get_db)):
    return IndustryService(db).create_industry(payload)

@router.put("/{industry_id}", response_model=IndustryResponse)
def update_industry(industry_id: int, payload: IndustryUpdate, db: Session = Depends(get_db)):
    try:
        return IndustryService(db).update_industry(industry_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{industry_id}")
def delete_industry(industry_id: int, db: Session = Depends(get_db)):
    try:
        return IndustryService(db).delete_industry(industry_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
