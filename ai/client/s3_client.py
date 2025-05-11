from client.api_client import ApiClient

api = ApiClient()
def get_presigned_url(filename, book_id, authorization):
    endpoint = f"/v1/book/{book_id}/story/image"    
    payload = {"filename": filename}
    result = api.request("POST", endpoint, authorization, payload)
    return result.get("presigned_url"), result.get("content_type")