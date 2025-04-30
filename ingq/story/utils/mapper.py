from story.domain.story import Story
from story.dto.schemas import CreateStoryResponse


class StoryMapper:
    @staticmethod
    def to_create_story_response(story: Story) -> CreateStoryResponse:
        return CreateStoryResponse(
            story_id=story.id,
            book_id=story.book_id,
            page_number=story.page_number,
            story_text=story.story_text,
            created_at=story.created_at,
            updated_at=story.updated_at,
        )
