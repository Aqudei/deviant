import pdb
from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import os


class DeviantArt:
    CLIENT_ID = ''
    CLIENT_SECRET = ''

    def __init__(self, *args, **kwargs):
        """
        docstring
        """
        self.CLIENT_ID = kwargs.get('client_id', settings.DA_CLIENT_ID)
        self.CLIENT_SECRET = kwargs.get(
            'client_secret', settings.DA_CLIENT_SECRET)

        client = BackendApplicationClient(client_id=self.CLIENT_ID)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url='https://www.deviantart.com/oauth2/token', client_id=self.CLIENT_ID,
                                  client_secret=self.CLIENT_SECRET)

        self.token = token

        print("Token:")
        print(self.token)
        self.session = OAuth2Session(
            client_id=self.CLIENT_ID, token=self.token)

    def get_profile(self, username):
        """
        docstring
        """
        params = {
            "expand": "user.stats"
        }
        url = f'https://www.deviantart.com/api/v1/oauth2/user/profile/{username}'
        response = self.session.get(url, params=params)
        if not response.status_code == 200:
            print(f"ERROR: {response.text}")
            return
        response_json = response.json()
        return response_json

    def list_watchers(self, username):
        """
        docstring
        """
        params = {
            "offset": 0,
            "limit": 50
        }
        url = f'https://www.deviantart.com/api/v1/oauth2/user/watchers/{username}'
        response = self.session.get(url, params=params)
        if not response.status_code == 200:
            print(f"ERROR: {response.text}")
            return

        response_json = response.json()
        while response_json.get('results') and len(response_json['results']) > 0:

            for r in response_json['results']:
                yield r

            if not response_json['has_more']:
                break

            params['offset'] = response_json['next_offset']
            response = self.session.get(url, params=params)
            if not response.status_code == 200:
                print(f"ERROR: {response.text}")
                break
            response_json = response.json()
