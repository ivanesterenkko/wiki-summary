from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.article import crud_article
from src.utilities.parser import WikiParserService


class ArticleService:
    async def parse_and_save(self, db: AsyncSession, url: str):
        count = await WikiParserService().parse(db, url)
        main_article = await crud_article.get_by_url(db, url)
        return main_article, count
