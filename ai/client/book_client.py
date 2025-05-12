from client.api_client import ApiClient

api = ApiClient()
#스토리 받아오는 함수
def get_story(book_id, page_number, authorization):
    endpoint = f"/v1/book/{book_id}/story/{page_number}"
    result = api.request("GET", endpoint, authorization)
    return result.get("story_text")

#모든 스토리 받아오는 함수 (임시)
def get_all_story(book_id, authorization):
    endpoint = f"/v1/book/{book_id}/story" #임시
    try:
        result = api.request("GET", endpoint, authorization)
        return result.get("story_text")
    except Exception as e:
        print(f"모든 스토리 조회 실패: {e}")
        return "이전 이야기가 없습니다."

#책 정보 받아오는 함수
def get_book(book_id, authorization):
    endpoint = f"/v1/book?bookid={book_id}"
    result = api.request("GET", endpoint, authorization)
    return result