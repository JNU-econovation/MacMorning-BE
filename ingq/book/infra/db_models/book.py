from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    genre: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    gamemode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    character: Mapped[dict] = mapped_column(JSON, nullable=False)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    background: Mapped[str] = mapped_column(String(100), nullable=False)
    is_storage: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
