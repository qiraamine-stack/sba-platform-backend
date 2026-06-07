def calculate_monthly_payment(loan_amount, annual_rate, term_years):
    monthly_rate = annual_rate / 100 / 12
    n_payments = term_years * 12
    if monthly_rate == 0:
        return round(loan_amount / n_payments, 2)
    payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
    return round(payment, 2)

def calculate_sba_7a(business_price, down_payment_pct=0.10):
    down_payment = round(business_price * down_payment_pct, 2)
    loan_amount = round(business_price - down_payment, 2)
    annual_rate = 11.5
    term_years = 10
    monthly_payment = calculate_monthly_payment(loan_amount, annual_rate, term_years)
    total_paid = round(monthly_payment * term_years * 12, 2)
    total_interest = round(total_paid - loan_amount, 2)
    return {
        "loan_type": "SBA 7(a)",
        "business_price": business_price,
        "down_payment": down_payment,
        "down_payment_pct": down_payment_pct * 100,
        "loan_amount": loan_amount,
        "interest_rate": annual_rate,
        "term_years": term_years,
        "monthly_payment": monthly_payment,
        "total_paid": total_paid,
        "total_interest": total_interest
    }

def calculate_dscr(annual_net_income, annual_debt_service):
    if annual_debt_service == 0:
        return None
    dscr = round(annual_net_income / annual_debt_service, 2)
    return {
        "dscr": dscr,
        "passes": dscr >= 1.25,
        "message": "Meets SBA minimum" if dscr >= 1.25 else "Below SBA minimum of 1.25"
    }

def check_sba_eligibility(business_price, annual_revenue, annual_net_income):
    issues = []
    if business_price > 5000000:
        issues.append("Business price exceeds SBA 7(a) maximum of $5M")
    if annual_revenue > 7500000:
        issues.append("Revenue may exceed SBA small business size standards")
    annual_debt = calculate_monthly_payment(business_price * 0.9, 11.5, 10) * 12
    dscr = calculate_dscr(annual_net_income, annual_debt)
    if dscr and not dscr["passes"]:
        issues.append(f"DSCR of {dscr['dscr']} is below SBA minimum of 1.25")
    return {
        "eligible": len(issues) == 0,
        "issues": issues,
        "dscr": dscr
    }