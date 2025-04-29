from sqlalchemy.orm import Session

from choice.domain.choice import Choice as ChoiceVO
from choice.domain.repository.choice_repository import ChoiceRepository
from choice.infra.db_models.choice import Choice


class MysqlChoiceRepository(ChoiceRepository):
    def save(self, choice: ChoiceVO, db: Session) -> ChoiceVO:
        new_choice = Choice(
            story_id=choice.story_id,
            first_choice=choice.first_choice,
            second_choice=choice.second_choice,
            third_choice=choice.third_choice,
            my_choice=choice.my_choice,
            is_success=choice.is_success,
            created_at=choice.created_at,
            updated_at=choice.updated_at,
        )
        db.add(new_choice)
        db.flush()
        return ChoiceVO(
            id=new_choice.id,
            story_id=new_choice.story_id,
            first_choice=new_choice.first_choice,
            second_choice=new_choice.second_choice,
            third_choice=new_choice.third_choice,
            my_choice=new_choice.my_choice,
            is_success=new_choice.is_success,
            created_at=new_choice.created_at,
            updated_at=new_choice.updated_at,
        )
