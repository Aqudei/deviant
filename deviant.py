from asyncio.log import logger
import pdb
from urllib import response
from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import os
import time


class DeviantArt:
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    BASE_URL = 'https://www.deviantart.com/api/v1/oauth2'
    DEFAULT_SLEEP = 16

    def __init__(self, user, *args, **kwargs):
        """
        docstring
        """
        self.user = user
        self.__authorize()

    def send_thanks(self, username):
        """
        Send thanks to Deviant
        """
        url = self.BASE_URL + f'/comments/post/profile/{username}'
        payload = {
            "body": "Thanks for the fav!"
        }

        time.sleep(self.DEFAULT_SLEEP)
        response = self.deviant.post(url, json=payload)
        if response.status_code == 200:
            return response.json()

        logger.error(response.text)

    def __authorize(self):
        """
        docstring
        """
        extra = {
            'client_id': settings.DA_CLIENT_ID,
            'client_secret': settings.DA_CLIENT_SECRET,
        }

        def token_updater(token):
            self.user.token = token
            self.user.save()

        self.deviant = OAuth2Session(
            client_id=settings.DA_CLIENT_ID,
            token=self.user.token,
            auto_refresh_kwargs=extra,
            auto_refresh_url=settings.DA_TOKEN_URL,
            token_updater=token_updater
        )

    def get_profile(self, username):
        """
        docstring
        """
        params = {
            "expand": "user.stats"
        }
        url = f'https://www.deviantart.com/api/v1/oauth2/user/profile/{username}'
        response = self.deviant.get(url, params=params)
        if not response.status_code == 200:
            print(f"ERROR: {response.text}")
        response_json = response.json()
        return response_json

    def list_favors(self, deviationid):
        """
        docstring
        """
        url = self.BASE_URL + "/deviation/whofaved"

        params = {
            "deviationid": deviationid,
            "limit": 50
        }

        for item in self.__list_items(url=url, params=params):
            yield item

    def list_deviations(self, username=None):
        """
        docstring
        """
        url = 'https://www.deviantart.com/api/v1/oauth2/collections/all'
        if username:
            url = f'https://www.deviantart.com/api/v1/oauth2/collections/all/{username}'
        params = {
            "limit": 24
        }
        for item in self.__list_items(url=url, params=params):
            yield item

    def list_watchers(self, username):
        """
        docstring
        """
        params = {
            "limit": 50
        }
        url = f'https://www.deviantart.com/api/v1/oauth2/user/watchers/{username}'
        for item in self.__list_items(url=url, params=params):
            yield item

    def __list_items(self, *args, **kwargs):
        """
        docstring
        """
        url = kwargs.pop('url', None)
        params = kwargs.pop('params', {})
        params['limit'] = params.get('limit', 10)
        params['offset'] = params.get('offset', 0)

        time.sleep(self.DEFAULT_SLEEP)
        response = self.deviant.get(url, params=params)

        if response.status_code == 429:
            logger.error("Rate limit reached!")
            return

        if not response.status_code == 200:
            logger.error(response.text)
            return

        response_json = response.json()
        while response_json.get('results') and len(response_json['results']) > 0:
            for r in response_json['results']:
                yield r

            if not response_json['has_more']:
                return

            params['offset'] = response_json['next_offset']
            time.sleep(self.DEFAULT_SLEEP)
            response = self.deviant.get(url, params=params)

            if response.status_code == 429:
                logger.error("Rate limit reached!")
                return

            if not response.status_code == 200:
                logger.error(f"{response.text}")
                return

            response_json = response.json()
