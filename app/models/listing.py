from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    industry = Column(String, nullable=False)
    location = Column(String)
    asking_price = Column(Float, nullable=False)
    annual_revenue = Column(Float)
    annual_net_income = Column(Float)
    sde = Column(Float)
    ebitda = Column(Float)
    year_established = Column(Integer)
    employees = Column(Integer)
    reason_for_sale = Column(String)
    sba_eligible = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    seller_name = Column(String)
    seller_email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())