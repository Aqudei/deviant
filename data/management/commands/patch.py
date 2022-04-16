import pdb
from textwrap import indent
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from deviant import DeviantArt
from data.models import *
from data import tasks
import json


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument("--marksent", action='store_true')
        parser.add_argument("--sentnow", action='store_true')
        parser.add_argument("--fetch-deviations", action='store_true')
        parser.add_argument("--fetch-favourites", action='store_true')
        parser.add_argument("--clear-watchers", action='store_true')

    def __savejson(self, obj, filename):
        """
        docstring
        """
        with open(filename, 'wt') as outfile:
            outfile.write(json.dumps(obj, indent=2))

    def handle(self, *args, **options):
        if options['clear_watchers']:
            for competitor in Competitor.objects.all():
                competitor.watchers.clear()

        if options['marksent']:
            Thank.objects.all().update(sent=True)

        if options['sentnow']:
            Thank.objects.all().update(sent_timestamp=timezone.now())

        if options['fetch_deviations']:
            tasks.cycle_deviations.apply_async()

        if options['fetch_favourites']:
            tasks.cycle_favorites.apply_async()
