"""Add story, illust, choice tables

Revision ID: 0b6babd9a2b0
Revises: 53c1a76b1fcf
Create Date: 2025-04-29 16:17:06.442763

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0b6babd9a2b0"
down_revision: Union[str, None] = "53c1a76b1fcf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "stories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=False),
        sa.Column("story_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "choices",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("story_id", sa.Integer(), nullable=False),
        sa.Column("first_choice", sa.String(length=127), nullable=False),
        sa.Column("second_choice", sa.String(length=127), nullable=False),
        sa.Column("third_choice", sa.String(length=255), nullable=True),
        sa.Column("my_choice", sa.Integer(), nullable=False),
        sa.Column("is_success", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["story_id"], ["stories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("story_id"),
    )
    op.create_table(
        "illusts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("story_id", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["story_id"], ["stories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("story_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("illusts")
    op.drop_table("choices")
    op.drop_table("stories")
    # ### end Alembic commands ###
