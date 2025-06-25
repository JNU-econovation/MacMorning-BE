from typing import Optional

from sqlalchemy.orm import Session

from choice.domain.choice import Choice as ChoiceVO
from choice.domain.repository.choice_repository import ChoiceRepository
from choice.infra.db_models.choice import Choice
from choice.utils.mapper import ChoiceMapper
from db.database import SessionLocal
from story.infra.db_models.story import Story


class MysqlChoiceRepository(ChoiceRepository):
    def save(self, choice: ChoiceVO, db: Session) -> ChoiceVO:
        new_choice = ChoiceMapper.choicevo_to_choice(choice)
        db.add(new_choice)
        db.flush()
        return ChoiceMapper.choice_to_choicevo(new_choice)

    def find_by_story_id(self, story_id: int, db: Session) -> Optional[ChoiceVO]:
        choice = db.query(Choice).filter(Choice.story_id == story_id).first()

        if not choice:
            return None

        return ChoiceMapper.choice_to_choicevo(choice)

    def find_all_by_book_id(self, book_id: int) -> list[Choice]:
        with SessionLocal() as db:
            choices = (
                db.query(Choice)
                .join(Choice.story)
                .filter(Story.book_id == book_id)
                .all()
            )
            return ChoiceMapper.choices_to_choicesvo(choices)

    def find_by_id(self, choice_id: int) -> ChoiceVO:
        with SessionLocal() as db:
            choice = db.query(Choice).filter(Choice.id == choice_id).first()

            if not choice:
                return None

            return ChoiceMapper.choice_to_choicevo(choice)

    def update_reason(self, choice: ChoiceVO) -> ChoiceVO:
        with SessionLocal() as db:
            db_choice = db.query(Choice).filter(Choice.id == choice.id).first()

            if not db_choice:
                return None

            db_choice.reason = choice.reason
            db.commit()

            return ChoiceMapper.choice_to_choicevo(db_choice)
