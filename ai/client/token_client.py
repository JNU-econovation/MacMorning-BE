from .api_client import ApiClient
import logging

api = ApiClient()
logger = logging.getLogger(__name__)


def token_verification(authorization):
    endpoint = f"v1/verification"    
    try:
        result = api.request("POST", endpoint, authorization)
        if result.get("success") :
            return True
        else :
            logger.debug(f"에러메시지 : {result.get('error')}")
            return False
    except Exception as e:
        logger.error(f"token 인증 실패 : {e}", exc_info=True)
        return False