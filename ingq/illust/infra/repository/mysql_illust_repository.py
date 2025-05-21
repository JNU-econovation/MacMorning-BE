from typing import Optional

from sqlalchemy.orm import Session

from illust.domain.illust import Illust as IllustVO
from illust.domain.repository.illust_repository import IllustRepository
from illust.infra.db_models.illust import Illust
from illust.utils.mapper import IllustMapper


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
