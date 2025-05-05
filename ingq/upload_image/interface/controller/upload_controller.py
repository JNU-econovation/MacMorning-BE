from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from book.application.book_service import BookService
from dependencies.containers import Container
from upload_image.application.file_service import FileService
from upload_image.application.s3_service import S3Service
from upload_image.dto.schemas import UploadImageRequest, UploadImageResponse

router = APIRouter(prefix="/v1", tags=["Upload Router"])


@router.post("/book/{book_id}/story/image")
@inject
def upload_image(
    request: Request,
    book_id: int,
    upload_image_request: UploadImageRequest,
    book_service: BookService = Depends(Provide[Container.book_service]),
    s3_service: S3Service = Depends(Provide[Container.s3_service]),
    file_service: FileService = Depends(Provide[Container.file_service]),
) -> UploadImageResponse:
    user_id = request.state.current_user.id

    book = book_service.get_book_by_id_or_throw(book_id)

    if book.user_id != user_id:
        raise Exception("Invalid user access")

    original_filename = upload_image_request.filename
    content_type = file_service.get_content_type(original_filename)
    unique_filename = file_service.generate_unique_filename(original_filename)

    presigned_url = s3_service.generate_presigned_url(
        key=unique_filename, content_type=content_type
    )

    return UploadImageResponse(
        presigned_url=presigned_url,
        filename=unique_filename,
        content_type=content_type,
    )
