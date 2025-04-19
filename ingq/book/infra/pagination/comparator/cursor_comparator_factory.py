from book.infra.pagination.order_strategy import OrderStrategy
from book.infra.pagination.comparator.created_at_desc_comparator import (
    CreatedAtDescComparator,
)
from book.infra.pagination.comparator.created_at_asc_comparator import (
    CreatedAtAscComparator,
)
from book.infra.pagination.comparator.updated_at_desc_comparator import (
    UpdatedAtDescComparator,
)
from book.infra.pagination.comparator.updated_at_asc_comparator import (
    UpdatedAtAscComparator,
)
from book.infra.pagination.comparator.cursor_comparator import CursorComparator


def get_cursor_comparator(strategy: OrderStrategy) -> CursorComparator:
    """
    TODO

    view count, bookmark count 정렬 기능 추가

    """
    if strategy == OrderStrategy.CREATED_AT_DESC:
        return CreatedAtDescComparator()
    elif strategy == OrderStrategy.CREATED_AT_ASC:
        return CreatedAtAscComparator()
    elif strategy == OrderStrategy.UPDATED_AT_DESC:
        return UpdatedAtDescComparator()
    elif strategy == OrderStrategy.UPDATED_AT_ASC:
        return UpdatedAtAscComparator()
    else:
        raise ValueError(f"Unsupported strategy: {strategy}")
