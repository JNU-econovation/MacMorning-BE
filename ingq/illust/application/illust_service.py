from datetime import datetime, timezone

from sqlalchemy.orm import Session

from illust.domain.illust import Illust
from illust.domain.repository.illust_repository import IllustRepository
from illust.dto.schemas import CreateIllustRequest, CreateIllustResponse


class IllustService:
    def __init__(self, illust_repository: IllustRepository):
        self.illust_repository = illust_repository

    def create_illust(
        self,
        story_id: int,
        create_illust_request: CreateIllustRequest,
        session: Session,
    ) -> CreateIllustResponse:
        now = datetime.now(timezone.utc)
        illust = Illust(
            id=None,
            story_id=story_id,
            image_url=create_illust_request.image_url,
            created_at=now,
            updated_at=now,
        )
        saved_illust = self.illust_repository.save(illust, db=session)

        return CreateIllustResponse(
            illust_id=saved_illust.id,
            story_id=saved_illust.story_id,
            image_url=saved_illust.image_url,
            created_at=saved_illust.created_at,
            updated_at=saved_illust.updated_at,
        )
