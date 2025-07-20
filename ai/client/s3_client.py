from .api_client import ApiClient
import logging

api = ApiClient()
logger = logging.getLogger(__name__)


def get_presigned_url(filename, book_id, authorization):
    endpoint = f"v1/book/{book_id}/story/image"    
    payload = {"filename": filename}
    try:
        result = api.request("POST", endpoint, authorization, payload)
        return result.get("presigned_url"), result.get("content_type"), result.get("filename")
    except Exception as e:
        logger.error(f"S3 presigned URL 요청 실패 : {e}", exc_info=True)
        raise