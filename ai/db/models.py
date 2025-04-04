from sqlalchemy import Column, Integer, String

from db.database import Base

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(300), nullable=False)
    pageNumber = Column(Integer, nullable=False)