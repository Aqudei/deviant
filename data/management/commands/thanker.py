import pdb
from textwrap import indent
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from deviant import DeviantArt
from data.models import DAUser, User
import json


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--offset', type=int, default=0)

    def __savejson(self, obj, filename):
        """
        docstring
        """
        with open(filename, 'wt') as outfile:
            outfile.write(json.dumps(obj, indent=2))

    def handle(self, *args, **options):
        da_username = settings.DA_USERNAME
        dj_user = User.objects.filter(da_username=da_username).first()

        da = DeviantArt(dj_user, options['offset'])

        watchers = da.list_watchers(da_username)
        for w in watchers:
            obj, created = DAUser.objects.update_or_create(
                username=w['user']['username'], defaults={
                    "user": dj_user,
                    "userid": w['user'].get('userid')
                })

            profile = da.get_profile(w['user']['username'])
            if profile:
                if 'stats' in profile:
                    obj.pageview_count = profile['stats']['profile_pageviews']
                    obj.deviations_count = profile['stats']['user_deviations']
                if 'stats' in profile['user']:
                    obj.watchers_count = profile['user']['stats']['watchers']
                # self.__savejson(profile, "./responses/profile.json")
                obj.save()
