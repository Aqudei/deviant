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
        with open("./creds", 'rb') as infile:
            cred = pickle.load(infile)

            session = OAuth2Session(settings.DA_CLIENT_ID, token=cred)
            import pdb
            pdb.set_trace()