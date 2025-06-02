from typing import Optional

from sqlalchemy.orm import Session

from db.database import SessionLocal
from illust.domain.illust import Illust as IllustVO
from illust.domain.repository.illust_repository import IllustRepository
from illust.infra.db_models.illust import Illust
from illust.utils.mapper import IllustMapper
from story.infra.db_models.story import Story


class MysqlIllustRepository(IllustRepository):
    def save(self, illust: IllustVO, db: Session) -> IllustVO:
        new_illust = IllustMapper.illustvo_to_illust(illust)
        db.add(new_illust)
        db.flush()
        return IllustMapper.illust_to_illustvo(new_illust)

    def find_by_story_id(self, story_id: int, db: Session) -> Optional[IllustVO]:
        illust = db.query(Illust).filter(Illust.story_id == story_id).first()

        if not illust:
            return None

        return IllustMapper.illust_to_illustvo(illust)

    def find_all_by_book_id(self, book_id: int) -> list[IllustVO]:
        with SessionLocal() as db:
            illusts = (
                db.query(Illust)
                .join(Illust.story)
                .filter(Story.book_id == book_id)
                .all()
            )
        return IllustMapper.illusts_to_illustsvo(illusts)
