from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request

from auth.application.jwt_token_provider import JwtTokenProvider
from auth.utils.user_extractor import get_optional_current_user
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
    cursor: Optional[str] = Query(None, description="커서 값"),
    book_service: BookService = Depends(Provide[Container.book_service]),
    jwt_token_provider: JwtTokenProvider = Depends(
        Provide[Container.jwt_token_provider]
    ),
) -> PaginatedBookItem:
    """
    **AccessToken 검사 필요 없는 엔드포인트**

    Cursor 기반 페이지네이션을 적용해 전체 책 목록 조회

    - limit: 페이지당 항목 수(default = 4)
    - order_strategy: 정렬 전략(생성일자, 업데이트일자 기준 오름,내림 차순 제공)
        - created_at_desc, updated_at_desc
        - created_at_asc, updated_at_asc
    - cursor: 이전 페이지의 마지막 항목에 대한 커서(null 가능)
        - base64로 인코딩된 값
    """
    current_user = get_optional_current_user(request, jwt_token_provider)
    user_id = current_user.id if current_user else None
    return book_service.get_all_books(
        user_id, limit=limit, order_strategy=order_strategy, cursor=cursor
    )


@router.get("/books/mybooks")
@inject
def get_mybooks(
    request: Request,
    limit: int = Query(4, ge=1, description="페이지당 항목 수"),
    order_strategy: OrderStrategy = Query(
        OrderStrategy.CREATED_AT_DESC, description="정렬 전략"
    ),
    cursor: Optional[str] = Query(None, description="커서 값"),
    progress: Optional[bool] = Query(None, description="이야기 진행중 여부"),
    book_service: BookService = Depends(Provide[Container.book_service]),
) -> PaginatedBookItem:
    """
    Cursor 기반 페이지네이션을 적용해 내가 쓴 책 목록 조회

    - limit: 페이지당 항목 수(default = 4)
    - order_strategy: 정렬 전략(생성일자, 업데이트일자 기준 오름,내림 차순 제공)
        - created_at_desc, updated_at_desc
        - created_at_asc, updated_at_asc
    - cursor: 이전 페이지의 마지막 항목에 대한 커서(null 가능)
        - base64로 인코딩된 값
    - progress: 이야기 진행 여부
        - True 이면 진행중인 이야기를, False 이면 완성된 이야기, None인 경우 전체 책 반환
    """
    user_id = request.state.current_user.id
    return book_service.get_mybooks(
        user_id,
        limit=limit,
        order_strategy=order_strategy,
        cursor=cursor,
        progress=progress,
    )


@router.get("/books/bookmarks")
@inject
def get_bookmarked_books(
    request: Request,
    limit: int = Query(4, ge=1, description="페이지당 항목 수"),
    order_strategy: OrderStrategy = Query(
        OrderStrategy.CREATED_AT_DESC, description="정렬 전략"
    ),
    cursor: Optional[str] = Query(None, description="커서 값"),
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    """
    Cursor 기반 페이지네이션을 적용해 내가 북마크한 책 목록 조회

    - limit: 페이지당 항목 수(default = 4)
    - order_strategy: 정렬 전략(생성일자, 업데이트일자 기준 오름,내림 차순 제공)
        - created_at_desc, updated_at_desc
        - created_at_asc, updated_at_asc
    - cursor: 이전 페이지의 마지막 항목에 대한 커서(null 가능)
        - base64로 인코딩된 값
    """
    user_id = request.state.current_user.id
    return book_service.get_bookmarked_books(
        user_id,
        limit=limit,
        order_strategy=order_strategy,
        cursor=cursor,
    )


@router.get("/books/best")
@inject
def get_best_books(
    request: Request,
    limit: int = Query(4, ge=1, description="페이지당 항목 수"),
    cursor: Optional[str] = Query(None, description="커서 값"),
    book_service: BookService = Depends(Provide[Container.book_service]),
    jwt_token_provider: JwtTokenProvider = Depends(
        Provide[Container.jwt_token_provider]
    ),
):
    """
    Cursor 기반 페이지네이션을 적용해 북마크순 책 목록 조회

    - limit: 페이지당 항목 수(default = 4)
    - cursor: 이전 페이지의 마지막 항목에 대한 커서(null 가능)
        - base64로 인코딩된 값
    """
    current_user = get_optional_current_user(request, jwt_token_provider)
    user_id = current_user.id if current_user else None
    return book_service.get_best_books(user_id, limit=limit, cursor=cursor)
