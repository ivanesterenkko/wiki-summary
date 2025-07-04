"""init

Revision ID: c484e939a43f
Revises:
Create Date: 2025-06-05 05:22:50.666888

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c484e939a43f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "article",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["article.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_article_id"), "article", ["id"], unique=False)
    op.create_index(
        op.f("ix_article_parent_id"), "article", ["parent_id"], unique=False
    )
    op.create_index(op.f("ix_article_url"), "article", ["url"], unique=True)
    op.create_table(
        "summary",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["article_id"], ["article.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_summary_article_id"), "summary", ["article_id"], unique=False
    )
    op.create_index(op.f("ix_summary_id"), "summary", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_summary_id"), table_name="summary")
    op.drop_index(op.f("ix_summary_article_id"), table_name="summary")
    op.drop_table("summary")
    op.drop_index(op.f("ix_article_url"), table_name="article")
    op.drop_index(op.f("ix_article_parent_id"), table_name="article")
    op.drop_index(op.f("ix_article_id"), table_name="article")
    op.drop_table("article")
    # ### end Alembic commands ###
