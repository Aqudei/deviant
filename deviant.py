import pdb
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json


class DeviantArt:

    CLIENT_ID = '18601'
    CLIENT_SECRET = 'f1188bd6484dc0310de7fc9aee0e752c'

    def list_watchers(self):
        """
        docstring
        """
        params = {
            "offset": 0,
            "limit": 50
        }
        url = 'https://www.deviantart.com/api/v1/oauth2/user/watchers/GrowGetter'
        response = self.session.get(url, params=params)
        if not response.status_code == 200:
            return

        response_json = response.json()
        while response_json.get('results'):

            for r in response_json['results']:
                yield r

            if not response_json['has_more']:
                break

            params['offset'] = response.json()['next_offset']
            response = self.session.get(url)
            if not response.status_code == 200:
                break
            response_json = response.json()

    def __init__(self):
        """
        docstring
        """
        client = BackendApplicationClient(client_id=self.CLIENT_ID)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url='https://www.deviantart.com/oauth2/token', client_id=self.CLIENT_ID,
                                  client_secret=self.CLIENT_SECRET)

        self.token = token

        print("Token:")
        print(self.token)
        self.session = OAuth2Session(
            client_id=self.CLIENT_ID, token=self.token)
