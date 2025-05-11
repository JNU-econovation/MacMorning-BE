from .api_client import ApiClient

api = ApiClient()
def get_presigned_url(filename, book_id, authorization):
    endpoint = f"/v1/book/{book_id}/story/image"    
    payload = {"filename": filename}
    try:
        result = api.request("POST", endpoint, authorization, payload)
        return result.get("presigned_url"), result.get("content_type")
    except Exception as e:
        raise RuntimeError(f"S3 presigned URL 요청 실패 : {e}") from e