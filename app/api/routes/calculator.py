from fastapi import APIRouter
from pydantic import BaseModel
from app.services.valuation import calculate_sde, get_valuation_range
from app.services.sba_loan import calculate_sba_7a, calculate_dscr, check_sba_eligibility

router = APIRouter()

class ValuationInput(BaseModel):
    revenue: float
    cogs: float
    operating_expenses: float
    owners_salary: float
    owners_benefits: float
    one_time_expenses: float
    industry: str

class LoanInput(BaseModel):
    business_price: float
    down_payment_pct: float = 0.10
    annual_net_income: float

@router.post("/valuate")
def valuate_business(data: ValuationInput):
    sde = calculate_sde(
        data.revenue, data.cogs, data.operating_expenses,
        data.owners_salary, data.owners_benefits, data.one_time_expenses
    )
    valuation = get_valuation_range(sde, data.industry)
    return {"sde": sde, "valuation": valuation, "industry": data.industry}

@router.post("/loan")
def calculate_loan(data: LoanInput):
    loan = calculate_sba_7a(data.business_price, data.down_payment_pct)
    eligibility = check_sba_eligibility(
        data.business_price, data.business_price * 2, data.annual_net_income
    )
    dscr = calculate_dscr(
        data.annual_net_income, loan["monthly_payment"] * 12
    )
    return {"loan": loan, "eligibility": eligibility, "dscr": dscr}