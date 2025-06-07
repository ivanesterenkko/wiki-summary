from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import Article
from src.crud.article import crud_article
from src.crud.summary import crud_summary
from src.schemas.summary import SummaryCreateDB
from src.utilities.openai import gpt_summarize


class SummaryService:
    async def generate_and_save(self, db: AsyncSession, article: Article):
        try:
            existing_summary = await crud_summary.get_by_article_id(
                db, article.id
            )
            if existing_summary:
                return existing_summary

            summary = await gpt_summarize(article.content)
            if not summary:
                raise RuntimeError(
                    "Сервис генерации summary вернул пустой результат"
                )

            return await crud_summary.create(
                db,
                create_schema=SummaryCreateDB(
                    content=summary,
                    article_id=article.id,
                ),
            )
        except HTTPException:
            raise
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при генерации summary: {ex!s}",
            ) from ex

    async def get_summary(self, db: AsyncSession, url: str):
        try:
            article = await crud_article.get_by_url(db, url)
            if not article:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Статья не найдена",
                )
            summary = await crud_summary.get_by_article_id(db, article.id)
            if not summary:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Summary для данной статьи не найден",
                )
            return summary
        except HTTPException:
            raise
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при получении summary: {ex!s}",
            ) from ex
