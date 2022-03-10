from datetime import datetime, timedelta
import os
import pdb
from textwrap import indent
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from deviant import DeviantArt
from data.models import *
import json
import pickle
from requests_oauthlib import OAuth2Session
from django.conf import settings
from data.models import *
import logging

logger = logging.getLogger(__name__)
BASE_URL = 'https://www.deviantart.com/api/v1/oauth2'


class Command(BaseCommand):
    help = ''

    def __authorize(self, user):
        """
        docstring
        """
        extra = {
            'client_id': settings.DA_CLIENT_ID,
            'client_secret': settings.DA_CLIENT_SECRET,
        }

        def token_updater(token):
            user.token = token
            user.save()

        self.deviant = OAuth2Session(
            client_id=settings.DA_CLIENT_ID,
            token=user.token,
            auto_refresh_kwargs=extra,
            auto_refresh_url=settings.DA_TOKEN_URL,
            token_updater=token_updater
        )

    def __init__(self, *args, **kwargs):
        pass

    def add_arguments(self, parser):
        parser.add_argument("user")
        parser.add_argument("--fetch-deviations")
        parser.add_argument("--process-favors", action='store_true')

    def __savejson(self, obj, filename):
        """
        docstring
        """
        fullname = os.path.join("./responses", filename)
        with open(fullname, 'wt') as outfile:
            outfile.write(json.dumps(obj, indent=2))

    def list_deviations(self, username=None):
        """
        docstring
        """
        params = {
            "username": username
        }
        url = BASE_URL + '/collections/all'
        response = self.deviant.get(url, params=params)
        response_json = response.json()
        if response.status_code != 200:
            logger.warning(response.text)
            yield
            return

        for dev in response_json["results"]:
            yield dev

        while response_json['has_more']:
            params["offset"] = response_json['next_offset']

            response = self.deviant.get(url, params=params)

            response_json = response.json()
            if response.status_code == 200:
                for dev in response_json["results"]:
                    yield dev

    def __get_items(self, url, params):
        """
        docstring
        """
        response = self.deviant.get(url, params=params)
        response_json = response.json()
        for r in response_json['results']:
            yield r

        while response_json['has_more']:
            params['offset'] = response_json['next_offset']
            response = self.deviant.get(url, params=params)
            response_json = response.json()
            for r in response_json['results']:
                yield r

    def whofaved(self, deviationid):
        """
        docstring
        """
        url = BASE_URL + "/deviation/whofaved"
        params = {
            "deviationid": deviationid
        }
        for item in self.__get_items(url, params):
            yield item

    def handle(self, *args, **options):
        owner = User.objects.get(da_username=options['user'])
        self.__authorize(owner)

        if options.get('fetch_deviations'):
            for dev in self.list_deviations(options.get('--fetch-deviations')):
                Deviation.objects.update_or_create(deviationid=dev['deviationid'], owner=owner, defaults={
                    "title": dev['title'],
                })

        if options.get('process_favors'):
            for dev in Deviation.objects.all():
                favors = self.whofaved(dev.deviationid)
                for f in favors:
                    user = f['user']
                    Favor.objects.get_or_create(
                        deviation=dev, userid=user['userid'], owner=owner)
