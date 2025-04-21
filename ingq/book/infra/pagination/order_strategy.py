from enum import StrEnum


class OrderStrategy(StrEnum):
    CREATED_AT_DESC = "created_at_desc"
    CREATED_AT_ASC = "created_at_asc"
    UPDATED_AT_DESC = "updated_at_desc"
    UPDATED_AT_ASC = "updated_at_asc"
    BOOKMARK_COUNT_DESC = "bookmark_count_desc"
    BOOKMARK_COUNT_ASC = "bookmark_count_asc"
