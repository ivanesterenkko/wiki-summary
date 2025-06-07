import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.database import get_async_master_session
from src.schemas.article import ArticleBase
from src.schemas.summary import SummaryResponse
from src.services.article import ArticleService
from src.services.summary import SummaryService
from src.utilities.valid_url import is_valid_wiki_url

router = APIRouter()


@router.post(
    "/parse",
    status_code=status.HTTP_201_CREATED,
)
async def parse_url(
    data: ArticleBase, db: AsyncSession = Depends(get_async_master_session)
) -> None:
    if not is_valid_wiki_url(data.url):
        raise HTTPException(
            status_code=400, detail="Некорректный URL Википедии"
        )
    article_service = ArticleService()
    try:
        main_article, count = await article_service.parse_and_save(
            db=db, url=data.url
        )
        if not main_article:
            raise HTTPException(
                status_code=404,
                detail="Главная статья не найдена после парсинга",
            )
        summary_service = SummaryService()
        await summary_service.generate_and_save(db, main_article)
    except httpx.ReadTimeout:
        raise HTTPException(
            status_code=504, detail="Timeout при обращении к Википедии"
        )
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"{ex!s}") from ex
    return {"message": f"Parsed {count} links from {data.url}."}


@router.get("/summary", response_model=SummaryResponse)
async def get_summary(
    url: str, db: AsyncSession = Depends(get_async_master_session)
):
    if not is_valid_wiki_url(url):
        raise HTTPException(
            status_code=400, detail="Некорректный URL Википедии"
        )
    try:
        return await SummaryService().get_summary(db, url=url)
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка на сервере: {ex!s}",
        ) from ex
