import pdb
from textwrap import indent
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from deviant import DeviantArt
from data.models import DAUser, User
import json
import pickle
from requests_oauthlib import OAuth2Session
from django.conf import settings
from data.models import *


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        pass

    def __savejson(self, obj, filename):
        """
        docstring
        """
        with open(filename, 'wt') as outfile:
            outfile.write(json.dumps(obj, indent=2))

    def handle(self, *args, **options):
        for user in User.objects.filter(da_userid__isnull=False).exclude(da_userid=''):
            deviant = OAuth2Session(client_id=settings.DA_CLIENT_ID,
                                    token=user.token)
            response = deviant.get(
                "https://www.deviantart.com/api/v1/oauth2/placebo")
            print(response.json())
