from choice.domain.choice import Choice as ChoiceVO
from choice.dto.schemas import CreateChoiceResponse
from choice.infra.db_models.choice import Choice


class ChoiceMapper:
    @staticmethod
    def to_create_choice_response(choice: ChoiceVO) -> CreateChoiceResponse:
        return CreateChoiceResponse(
            choice_id=choice.id,
            story_id=choice.story_id,
            first_choice=choice.first_choice,
            second_choice=choice.second_choice,
            third_choice=choice.third_choice,
            my_choice=choice.my_choice,
            is_success=choice.is_success,
            created_at=choice.created_at,
            updated_at=choice.updated_at,
        )

    # Infra 계층에서 사용하는 메서드
    @staticmethod
    def choicevo_to_choice(choice: ChoiceVO) -> Choice:
        return Choice(
            id=choice.id,
            story_id=choice.story_id,
            first_choice=choice.first_choice,
            second_choice=choice.second_choice,
            third_choice=choice.third_choice,
            my_choice=choice.my_choice,
            is_success=choice.is_success,
            created_at=choice.created_at,
            updated_at=choice.updated_at,
        )

    @staticmethod
    def choice_to_choicevo(choice: Choice) -> ChoiceVO:
        return ChoiceVO(
            id=choice.id,
            story_id=choice.story_id,
            first_choice=choice.first_choice,
            second_choice=choice.second_choice,
            third_choice=choice.third_choice,
            my_choice=choice.my_choice,
            is_success=choice.is_success,
            created_at=choice.created_at,
            updated_at=choice.updated_at,
        )
