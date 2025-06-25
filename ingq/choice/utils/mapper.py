from choice.domain.choice import Choice as ChoiceVO
from choice.dto.schemas import (
    ChoiceItem,
    CreateChoiceResponse,
    LastChoiceItem,
)
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
            reason=choice.reason,
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
            reason=choice.reason,
            created_at=choice.created_at,
            updated_at=choice.updated_at,
        )

    @staticmethod
    def choices_to_choicesvo(choices: list[Choice]) -> list[ChoiceVO]:
        return [ChoiceMapper.choice_to_choicevo(choice) for choice in choices]

    # Domain 계층에서 사용하는 메서드
    @staticmethod
    def choicevo_to_choice_item(choice: ChoiceVO) -> ChoiceItem:
        return ChoiceItem(
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

    @staticmethod
    def choicevo_to_last_choice_item(
        choice: ChoiceVO, choice_content: str
    ) -> LastChoiceItem:
        return LastChoiceItem(
            choice_id=choice.id,
            story_id=choice.story_id,
            choice_content=choice_content,
            my_choice=choice.my_choice,
            is_success=choice.is_success,
            reason=choice.reason,
            created_at=choice.created_at,
            updated_at=choice.updated_at,
        )
