from datetime import datetime

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base
from user.domain.provider import Provider


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=True)
    nickname: Mapped[str] = mapped_column(String(10), nullable=False)
    profile_image: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        server_default="https://www.gravatar.com/avatar/?d=mp",
    )
    username: Mapped[str] = mapped_column(String(10), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    provider: Mapped[Provider] = mapped_column(Enum(Provider), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    bookmarks = relationship("Bookmark", back_populates="user")
