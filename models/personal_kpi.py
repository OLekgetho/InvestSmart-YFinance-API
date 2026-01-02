from typing import Optional
from pydantic import BaseModel

class PersonalKpi(BaseModel):
    marketCap: Optional[str]
    revenue: Optional[str]
    netIncome: Optional[str]
    fouryearNetIncomeAvg: Optional[str]
    trailingpe:Optional[str]
    fourYearAveragePE:Optional[str]
    pricetosaleratio: Optional[str]
    profitMarginTTM: Optional[str]
    fouryearProfitMargin: Optional[str]
    grossProfitMargin: Optional[str]
    freeCashFlowTTM: Optional[str]
    fouryearFreeCashFlow: Optional[str]
    pEFreeCashFlow: Optional[str]
    fouryearPEFreeCashFlow: Optional[str]
