from client.api_client import ApiClient
import logging

api = ApiClient()
logger = logging.getLogger(__name__)
#스토리 받아오는 함수
def get_story(book_id, page_number, authorization):
    endpoint = f"v1/book/{book_id}/story/{page_number}"
    result = api.request("GET", endpoint, authorization)
    story = result.get("story")
    if story:
        return story.get("story_text")
    return None

#모든 스토리 받아오는 함수 (임시)
def get_all_story(book_id, authorization):
    endpoint = f"v1/book/{book_id}/story" #임시
    try:
        result = api.request("GET", endpoint, authorization)
        return result.get("story_text")
    except Exception as e:
        logger.error(f"모든 스토리 조회 실패: {e}", exc_info=True)
        raise

#책 정보 받아오는 함수
def get_book(book_id, authorization):
    endpoint = f"v1/book/{book_id}"
    result = api.request("GET", endpoint, authorization)
    return result