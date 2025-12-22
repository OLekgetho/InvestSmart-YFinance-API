from pydantic import BaseModel
from typing import Optional

class Company(BaseModel):
    symbol : Optional[str]
    displayName: Optional[str]
    shortName: Optional[str]
    regularMarketPrice: Optional[float]
    regularMarketPreviousClose: Optional[float]
    regularMarketChange: Optional[float]
    regularMarketChangePercent: Optional[float]
    fiveYrDate: Optional[str]
    fiveYrPercentage: Optional[float]
    fiveYrDiff: Optional[float]

