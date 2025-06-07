from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.async_crud import BaseAsyncCRUD
from models import Article
from src.schemas.article import ArticleCreateDB, ArticleUpdateDB


class CRUDArticle(BaseAsyncCRUD[Article, ArticleCreateDB, ArticleUpdateDB]):
    async def get_by_url(
        self, db: AsyncSession, url: str
    ) -> Optional[Article]:
        stmt = (
            select(self.model)
            .where(self.model.url == url)
            .options(selectinload(self.model.children))
        )
        result = await db.execute(stmt)
        return result.scalars().first()


crud_article = CRUDArticle(Article)
