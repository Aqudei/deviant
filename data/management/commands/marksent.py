import pdb
from textwrap import indent
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from deviant import DeviantArt
from data.models import *
import json


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

        Thank.objects.all().update(sent=True)
