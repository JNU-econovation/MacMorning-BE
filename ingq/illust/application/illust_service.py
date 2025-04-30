from datetime import datetime, timezone

from sqlalchemy.orm import Session

from illust.domain.illust import Illust
from illust.domain.repository.illust_repository import IllustRepository
from illust.dto.schemas import CreateIllustRequest, CreateIllustResponse
from illust.utils.mapper import IllustMapper


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
        illust = Illust.create_illust_request_to_illust(
            story_id, create_illust_request, now
        )
        saved_illust = self.illust_repository.save(illust, db=session)

        return IllustMapper.to_create_illust_response(saved_illust)
