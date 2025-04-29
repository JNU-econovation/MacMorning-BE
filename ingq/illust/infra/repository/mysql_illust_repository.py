from sqlalchemy.orm import Session

from illust.domain.illust import Illust as IllustVO
from illust.domain.repository.illust_repository import IllustRepository
from illust.infra.db_models.illust import Illust


class MysqlIllustRepository(IllustRepository):
    def save(self, illust: IllustVO, db: Session) -> IllustVO:
        new_illust = Illust(
            story_id=illust.story_id,
            image_url=illust.image_url,
            created_at=illust.created_at,
            updated_at=illust.updated_at,
        )
        db.add(new_illust)
        db.flush()
        return IllustVO(
            id=new_illust.id,
            story_id=new_illust.story_id,
            image_url=new_illust.image_url,
            created_at=new_illust.created_at,
            updated_at=new_illust.updated_at,
        )
