from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db, Base, engine
from app.models.listing import Listing
from app.services.sba_loan import check_sba_eligibility
from app.services.email import send_new_listing_notification

Base.metadata.create_all(bind=engine)

router = APIRouter()

class ListingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    industry: str
    location: Optional[str] = None
    asking_price: float
    annual_revenue: Optional[float] = None
    annual_net_income: Optional[float] = None
    sde: Optional[float] = None
    ebitda: Optional[float] = None
    monthly_rent: Optional[float] = None
    monthly_expenses: Optional[float] = None
    employees: Optional[int] = None
    real_estate_included: Optional[bool] = False
    year_established: Optional[int] = None
    reason_for_sale: Optional[str] = None
    seller_name: str
    seller_email: str

@router.get("/")
def get_listings(
    industry: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sba_eligible: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Listing).filter(Listing.is_active == True)
    if industry:
        query = query.filter(Listing.industry == industry)
    if min_price:
        query = query.filter(Listing.asking_price >= min_price)
    if max_price:
        query = query.filter(Listing.asking_price <= max_price)
    if sba_eligible is not None:
        query = query.filter(Listing.sba_eligible == sba_eligible)
    return query.all()

@router.get("/{listing_id}")
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.post("/")
def create_listing(data: ListingCreate, db: Session = Depends(get_db)):
    eligibility = check_sba_eligibility(
        data.asking_price,
        data.annual_revenue or 0,
        data.annual_net_income or 0
    )
    listing = Listing(
        **data.dict(),
        sba_eligible=eligibility["eligible"]
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    send_new_listing_notification(listing.title, listing.asking_price, listing.seller_name, listing.seller_email, listing.industry)
    return listing

@router.delete("/{listing_id}")
def delete_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    listing.is_active = False
    db.commit()
    return {"message": "Listing removed"}
