from fastapi import APIRouter, Depends, Request

from dependency_injector.wiring import inject, Provide
from dependencies.containers import Container

from book.application.book_service import BookService

from book.dto.schemas import CreateBookRequest, CreateBookResponse


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
