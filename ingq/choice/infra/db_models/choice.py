from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Choice(Base):
    __tablename__ = "choices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    story_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("stories.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    first_choice: Mapped[str] = mapped_column(String(127), nullable=False)
    second_choice: Mapped[str] = mapped_column(String(127), nullable=False)
    third_choice: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    my_choice: Mapped[int] = mapped_column(Integer, nullable=False)
    is_success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    story = relationship("Story", back_populates="choice")

    __table_args__ = (CheckConstraint("my_choice IN (1, 2, 3)", name="_my_choice_ck"),)
