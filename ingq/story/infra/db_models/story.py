from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)
    story_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    book = relationship("Book", backref="stories")
    illust = relationship(
        "Illust",
        back_populates="story",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    choice = relationship(
        "Choice",
        back_populates="story",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
