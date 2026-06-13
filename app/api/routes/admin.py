from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.listing import Listing

router = APIRouter()

@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.created_at.desc()).all()

@router.get("/listings")
def get_all_listings(db: Session = Depends(get_db)):
    return db.query(Listing).order_by(Listing.created_at.desc()).all()
