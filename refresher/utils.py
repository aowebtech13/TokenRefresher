import requests
import os
from django.conf import settings

TOKENS_FILE = 'TOKENS.txt'
AXIOM_REFRESH_URL = os.getenv('AXIOM_REFRESH_URL')
AXIOM_REFRESH_TOKEN = os.getenv('AXIOM_REFRESH_TOKEN')

def refresh_axiom_tokens():
    """
    Calls Axiom's refresh endpoint and writes tokens to TOKENS.txt.
    """
    try:
        response = requests.post(
            AXIOM_REFRESH_URL,
            json={'refresh_token': AXIOM_REFRESH_TOKEN},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        # Assume the response contains 'access_token' and 'refresh_token'
        access_token = data.get('access_token')
        
        if access_token:
            with open(TOKENS_FILE, 'w') as f:
                f.write(access_token)
            return True, "Successfully refreshed tokens."
        else:
            return False, "Access token not found in response."
            
    except Exception as e:
        return False, f"Error refreshing tokens: {str(e)}"
