from typing import Optional

from pydantic import BaseModel


class News(BaseModel):
    title: Optional[str]
    publishedAt: Optional[str]
    source: Optional[str]
    url: Optional[str]