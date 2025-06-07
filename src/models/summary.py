from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models import Article


class Summary(Base):
    __tablename__ = "summary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str]
    article_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("article.id", ondelete="CASCADE"), index=True
    )
    article: Mapped["Article"] = relationship(
        "Article", back_populates="summary"
    )
