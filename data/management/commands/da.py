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
from data import tasks
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
        parser.add_argument("--fetch-deviations", action='store_true')
        parser.add_argument("--process-favors", action='store_true')
        parser.add_argument("--prepare-messages", action='store_true')
        parser.add_argument("--do-send", action='store_true')

    def __savejson(self, obj, filename):
        """
        docstring
        """
        fullname = os.path.join("./responses", filename)
        with open(fullname, 'wt') as outfile:
            outfile.write(json.dumps(obj, indent=2))

    def handle(self, *args, **options):
        if options.get('fetch_deviations'):
            tasks.cycle_deviations()
        if options.get('prepare_messages'):
            tasks.cycle_prepmsg()
        if options['do_send']:
            try:
                tasks.cycle_sender()
            except Exception as e:
                logger.exception(e)
