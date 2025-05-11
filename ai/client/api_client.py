from dotenv import load_dotenv
import requests
import os
load_dotenv()
class ApiClient :
    def __init__(self) :
        self.base_url = os.getenv("BE_BASE_URL")

    #be와 통신하는 기본 코드
    def request(self, method: str, endpoint: str, authorization: str, payload: dict[str, any]=None) :
        headers = {}
        if authorization:
            headers["Authorization"] = authorization
        
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method = method,
                url = url, 
                json = payload,
                headers = headers)
            print(response.request)
            response.raise_for_status()

            
            return response.json().get("data")
        
        except requests.exceptions.RequestException as e:
            print(f"{endpoint} 호출 중 오류 발생: {str(e)}")
            raise