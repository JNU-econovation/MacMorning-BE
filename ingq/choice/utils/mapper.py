from choice.domain.choice import Choice
from choice.dto.schemas import CreateChoiceResponse


class ChoiceMapper:
    @staticmethod
    def to_create_choice_response(choice: Choice) -> CreateChoiceResponse:
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
