from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from crud.async_crud import BaseAsyncCRUD
from models import Summary
from src.schemas.summary import SummaryCreateDB, SummaryUpdateDB


class CRUDSummary(BaseAsyncCRUD[Summary, SummaryCreateDB, SummaryUpdateDB]):
    async def get_by_article_id(
        self, db: AsyncSession, article_id: int
    ) -> Optional[Summary]:
        stmt = (
        select(self.model)
        .where(self.model.article_id == article_id)
    )
        result = await db.execute(stmt)
        return result.scalars().first()


crud_summary = CRUDSummary(Summary)