from sqlalchemy.orm import Session

from illust.domain.illust import Illust as IllustVO
from illust.domain.repository.illust_repository import IllustRepository
from illust.utils.mapper import IllustMapper


class MysqlIllustRepository(IllustRepository):
    def save(self, illust: IllustVO, db: Session) -> IllustVO:
        new_illust = IllustMapper.illustvo_to_illust(illust)
        db.add(new_illust)
        db.flush()
        return IllustMapper.illust_to_illustvo(new_illust)
