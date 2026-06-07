def calculate_sde(revenue, cogs, operating_expenses, owners_salary, owners_benefits, one_time_expenses):
    gross_profit = revenue - cogs
    ebitda = gross_profit - operating_expenses
    sde = ebitda + owners_salary + owners_benefits + one_time_expenses
    return round(sde, 2)

def calculate_valuation(sde, industry_multiple):
    return round(sde * industry_multiple, 2)

def calculate_ebitda(revenue, cogs, operating_expenses, depreciation, amortization):
    gross_profit = revenue - cogs
    ebitda = gross_profit - operating_expenses + depreciation + amortization
    return round(ebitda, 2)

INDUSTRY_MULTIPLES = {
    "restaurant": 1.5,
    "retail": 2.0,
    "service": 2.5,
    "healthcare": 3.0,
    "technology": 4.0,
    "manufacturing": 3.5,
    "construction": 2.5,
    "transportation": 2.0,
    "other": 2.5
}

def get_valuation_range(sde, industry):
    base = INDUSTRY_MULTIPLES.get(industry, 2.5)
    low = round(sde * (base - 0.5), 2)
    mid = round(sde * base, 2)
    high = round(sde * (base + 0.5), 2)
    return {"low": low, "mid": mid, "high": high, "multiple_used": base}