from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models import (
        Summary
    )


class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String, unique=True, index=True)
    title: Mapped[str]
    content: Mapped[str]
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("article.id", ondelete="SET NULL"), index=True
    )
    parent: Mapped[Optional["Article"]] = relationship(
        "Article", back_populates="children", remote_side=[id]
    )
    children: Mapped[List["Article"]] = relationship(
        "Article", back_populates="parent"
    )
    summary: Mapped["Summary"] = relationship(
        "Summary", back_populates="article", cascade="all, delete-orphan"
    )

