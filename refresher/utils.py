import requests
import logging
from django.conf import settings
from .models import TokenRefreshLog

logger = logging.getLogger(__name__)

def refresh_axiom_tokens():
    """
    Calls Axiom's refresh endpoint and writes tokens to the configured file.
    Also logs the attempt to the database.
    """
    url = settings.AXIOM_REFRESH_URL
    refresh_token = settings.AXIOM_REFRESH_TOKEN
    file_path = settings.TOKENS_FILE_PATH

    if not url or not refresh_token:
        error_msg = "Axiom settings are missing in environment."
        TokenRefreshLog.objects.create(success=False, message=error_msg)
        return False, error_msg

    try:
        response = requests.post(
            url,
            json={'refresh_token': refresh_token},
            timeout=10
        )
        status_code = response.status_code
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access_token')
            
            if access_token:
                with open(file_path, 'w') as f:
                    f.write(access_token)
                
                TokenRefreshLog.objects.create(success=True, message="Successfully refreshed tokens.", status_code=status_code)
                logger.info("Successfully refreshed tokens.")
                return True, "Successfully refreshed tokens."
            else:
                msg = "Access token not found in Axiom response."
                TokenRefreshLog.objects.create(success=False, message=msg, status_code=status_code)
                logger.error(msg)
                return False, msg
        else:
            msg = f"Failed to refresh tokens. Status: {status_code}"
            TokenRefreshLog.objects.create(success=False, message=msg, status_code=status_code)
            logger.error(msg)
            return False, msg
            
    except requests.exceptions.RequestException as e:
        msg = f"Network error: {str(e)}"
        TokenRefreshLog.objects.create(success=False, message=msg)
        logger.error(f"Network error refreshing tokens: {e}")
        return False, msg
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        TokenRefreshLog.objects.create(success=False, message=msg)
        logger.exception("Unexpected error refreshing tokens")
        return False, msg
