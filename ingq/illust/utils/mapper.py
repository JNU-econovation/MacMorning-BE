from illust.domain.illust import Illust as IllustVO
from illust.dto.schemas import CreateIllustResponse
from illust.infra.db_models.illust import Illust


class IllustMapper:
    @staticmethod
    def to_create_illust_response(illust: IllustVO) -> CreateIllustResponse:
        return CreateIllustResponse(
            illust_id=illust.id,
            story_id=illust.story_id,
            image_url=illust.image_url,
            created_at=illust.created_at,
            updated_at=illust.updated_at,
        )

    # Infra 계층에서 사용하는 메서드
    @staticmethod
    def illustvo_to_illust(illust: IllustVO) -> Illust:
        return Illust(
            id=illust.id,
            story_id=illust.story_id,
            image_url=illust.image_url,
            created_at=illust.created_at,
            updated_at=illust.updated_at,
        )

    @staticmethod
    def illust_to_illustvo(illust: Illust) -> IllustVO:
        return IllustVO(
            id=illust.id,
            story_id=illust.story_id,
            image_url=illust.image_url,
            created_at=illust.created_at,
            updated_at=illust.updated_at,
        )
