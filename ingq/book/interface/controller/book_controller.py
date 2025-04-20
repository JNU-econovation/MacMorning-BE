from typing import Any, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request

from book.application.book_service import BookService
from book.dto.schemas import CreateBookRequest, CreateBookResponse, PaginatedBookItem
from book.infra.pagination.order_strategy import OrderStrategy
from dependencies.containers import Container

router = APIRouter(prefix="/v1", tags=["Book Router"])


@router.post("/book", status_code=201)
@inject
def create_book(
    request: Request,
    create_book_request: CreateBookRequest,
    book_service: BookService = Depends(Provide[Container.book_service]),
) -> CreateBookResponse:
    current_user = request.state.current_user
    return book_service.create_book(current_user.id, create_book_request)


@router.get("/books", status_code=200)
@inject
def get_all_books(
    request: Request,
    limit: int = Query(4, ge=1, description="페이지당 항목 수"),
    order_strategy: OrderStrategy = Query(
        OrderStrategy.CREATED_AT_DESC, description="정렬 전략"
    ),
    cursor: Optional[Any] = Query(None, description="커서 값"),
    book_service: BookService = Depends(Provide[Container.book_service]),
) -> PaginatedBookItem:
    """
    **AccessToken 검사 필요 없는 엔드포인트**

    Cursor 기반 페이지네이션을 적용해 전체 책 목록 조회
    - limit: 페이지당 항목 수(default = 4)
    - order_strategy: 정렬 전략(생성일자, 업데이트일자, 조회수, 북마크 기준 오름,내림 차순 제공)
        - created_at_desc, updated_at_desc, bookmark_count_desc, view_count_desc
        - created_at_asc, updated_at_asc, bookmark_count_asc, view_count_asc
    - cursor: 이전 페이지의 마지막 항목에 대한 커서(null 가능)
        - 입력 예시
          created_at:2025-04-18T09:37:21,book_id:2
    """
    user_id = request.state.current_user.id if request.state.current_user else None
    return book_service.get_all_books(
        user_id, limit=limit, order_strategy=order_strategy, cursor=cursor
    )
