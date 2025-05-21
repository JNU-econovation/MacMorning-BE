from typing import Optional

from sqlalchemy.orm import Session

from choice.domain.choice import Choice as ChoiceVO
from choice.domain.repository.choice_repository import ChoiceRepository
from choice.infra.db_models.choice import Choice
from choice.utils.mapper import ChoiceMapper


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
