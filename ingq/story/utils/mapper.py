from story.domain.story import Story as StoryVO
from story.dto.schemas import CreateStoryResponse
from story.infra.db_models.story import Story


class StoryMapper:
    @staticmethod
    def to_create_story_response(story: StoryVO) -> CreateStoryResponse:
        return CreateStoryResponse(
            story_id=story.id,
            book_id=story.book_id,
            page_number=story.page_number,
            story_text=story.story_text,
            created_at=story.created_at,
            updated_at=story.updated_at,
        )

    # Infra 계층에서 사용하는 메서드
    @staticmethod
    def storyvo_to_story(story: StoryVO) -> Story:
        return Story(
            id=story.id,
            book_id=story.book_id,
            page_number=story.page_number,
            story_text=story.story_text,
            created_at=story.created_at,
            updated_at=story.updated_at,
        )

    @staticmethod
    def story_to_storyvo(story: Story) -> StoryVO:
        return StoryVO(
            id=story.id,
            book_id=story.book_id,
            page_number=story.page_number,
            story_text=story.story_text,
            created_at=story.created_at,
            updated_at=story.updated_at,
        )
