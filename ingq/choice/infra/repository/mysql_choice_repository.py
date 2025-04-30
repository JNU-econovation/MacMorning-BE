from sqlalchemy.orm import Session

from choice.domain.choice import Choice as ChoiceVO
from choice.domain.repository.choice_repository import ChoiceRepository
from choice.utils.mapper import ChoiceMapper


class MysqlChoiceRepository(ChoiceRepository):
    def save(self, choice: ChoiceVO, db: Session) -> ChoiceVO:
        new_choice = ChoiceMapper.choicevo_to_choice(choice)
        db.add(new_choice)
        db.flush()
        return ChoiceMapper.choice_to_choicevo(new_choice)
