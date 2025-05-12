from typing import Any
from dotenv import load_dotenv
import requests
import os
load_dotenv()
class ApiClient :
    def __init__(self) :
        self.base_url = os.getenv("BE_BASE_URL")
        if not self.base_url :
            raise RuntimeError("환경 변수 BE_BASE_URL이 설정되지 않았습니다.")

    #be와 통신하는 기본 코드
    def request(self, method: str, endpoint: str, authorization: str | None , payload: dict[str, Any] | None = None) -> Any :
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if authorization:
            headers["Authorization"] = authorization
        
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method = method,
                url = url, 
                json = payload,
                headers = headers)
            response.raise_for_status()

            
            return response.json().get("data")
        
        except requests.exceptions.RequestException as e:
            print(f"{endpoint} 호출 중 오류 발생: {str(e)}")
            raise