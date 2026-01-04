from typing import Optional
from pydantic import BaseModel

class PersonalKpi(BaseModel):
    marketCap: Optional[str]
    revenue: Optional[str]
    netIncome: Optional[str]
    fouryearNetIncomeAvg: Optional[str]
    trailingpe:Optional[str]
    pricetosaleratio: Optional[str]
    profitMarginTTM: Optional[str]
    fouryearProfitMargin: Optional[str]
    grossProfitMargin: Optional[str]
    freeCashFlowTTM: Optional[str]
    fouryearFreeCashFlow: Optional[str]
    pEFreeCashFlow: Optional[str]
    enterpriseValue: Optional[str]
    fcf_to_net_income: Optional[str]
    netDebt: Optional[str]
    revenue_cagr: Optional[str]
    net_income_cagr:Optional[str]
    fcf_cagr: Optional[str]
