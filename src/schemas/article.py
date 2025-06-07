from typing import Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    url: str


class ArticleCreateDB(ArticleBase):
    parent_id: Optional[int] = None
    title: str
    content: str


class ArticleResponse(ArticleCreateDB):
    id: int


class ArticleUpdateDB(BaseModel):
    pass
