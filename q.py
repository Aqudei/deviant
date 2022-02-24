import deviant
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID')
REDIRECT_URL = os.environ.get('DA_REDIRECT_URL')
authorization_base_url = 'https://www.deviantart.com/oauth2/authorize'

# REDIRECT_URL = 'http://143.198.179.20/oauthlogin'

if __name__ == "__main__":
    # client = deviant.DeviantArt()
    # client.list_watchers()
    
    scope = 'comment.post'
    deviant = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URL)
    authorization_url, state = deviant.authorization_url(
        authorization_base_url)

    
    print(authorization_url)
