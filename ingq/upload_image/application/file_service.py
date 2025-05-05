import mimetypes
import os
import re

import ulid

from upload_image.exception.file_exception import (
    InvalidExtTypeException,
    InvalidFilenameCharacterException,
    InvalidFilenameLengthException,
)


class FileService:
    @staticmethod
    def get_content_type(filename: str) -> str:
        content_type = mimetypes.guess_type(filename)[0]

        if content_type:
            return content_type

        ext = os.path.splitext(filename)[1].lower()
        content_type_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }

        if ext not in content_type_map:
            raise InvalidExtTypeException()

        return content_type_map.get(ext)

    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        if len(original_filename) > 50:
            raise InvalidFilenameLengthException()

        if not all(c.isalnum() or c in "_.-" for c in original_filename):
            raise InvalidFilenameCharacterException()

        return f"{ulid.ULID().generate()}_{original_filename}"
