from sqlalchemy.orm import Session

from story.domain.repository.story_repository import StoryRepository
from story.domain.story import Story as StoryVO
from story.infra.db_models.story import Story


class MysqlStoryRepository(StoryRepository):
    def save(self, story: StoryVO, db: Session) -> StoryVO:
        new_story = Story(
            book_id=story.book_id,
            page_number=story.page_number,
            story_text=story.story_text,
            created_at=story.created_at,
            updated_at=story.updated_at,
        )
        db.add(new_story)
        db.flush()
        return StoryVO(
            id=new_story.id,
            book_id=new_story.book_id,
            page_number=new_story.page_number,
            story_text=new_story.story_text,
            created_at=new_story.created_at,
            updated_at=new_story.updated_at,
        )
