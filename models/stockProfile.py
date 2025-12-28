from typing import Optional

from pydantic import BaseModel


class StockProfile(BaseModel):
    phone: Optional[str]
    website: Optional[str]
    fullTimeEmployees: Optional[int]
    marketCap: Optional[float]
    shortName: Optional[str]
    currency: Optional[str]
    symbol: Optional[str]
    country: Optional[str]
    sector: Optional[str]