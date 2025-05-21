from typing import Optional

from sqlalchemy.orm import Session

from db.database import SessionLocal
from story.domain.repository.story_repository import StoryRepository
from story.domain.story import Story as StoryVO
from story.infra.db_models.story import Story
from story.utils.mapper import StoryMapper


class MysqlStoryRepository(StoryRepository):
    def save(self, story: StoryVO, db: Session) -> StoryVO:
        new_story = StoryMapper.storyvo_to_story(story)
        db.add(new_story)
        db.flush()
        return StoryMapper.story_to_storyvo(new_story)

    def find_by_book_id_and_page_number(
        self, book_id: int, page_number: int, db: Optional[Session] = None
    ) -> Optional[StoryVO]:
        if db is not None:
            story = (
                db.query(Story)
                .filter(Story.book_id == book_id, Story.page_number == page_number)
                .first()
            )
        else:
            with SessionLocal() as local_db:
                story = (
                    local_db.query(Story)
                    .filter(Story.book_id == book_id, Story.page_number == page_number)
                    .first()
                )

        if not story:
            return None

        return StoryMapper.story_to_storyvo(story)
