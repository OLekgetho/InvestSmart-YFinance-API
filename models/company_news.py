from typing import Optional, List

from pydantic import BaseModel

from models.news import News


class CompanyNews(BaseModel):
  items: List[News]


