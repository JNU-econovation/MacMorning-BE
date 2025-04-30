from illust.domain.illust import Illust
from illust.dto.schemas import CreateIllustResponse


class IllustMapper:
    @staticmethod
    def to_create_illust_response(illust: Illust) -> CreateIllustResponse:
        return CreateIllustResponse(
            illust_id=illust.id,
            story_id=illust.story_id,
            image_url=illust.image_url,
            created_at=illust.created_at,
            updated_at=illust.updated_at,
        )
