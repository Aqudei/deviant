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
        pass

    def __savejson(self, obj, filename):
        """
        docstring
        """
        with open(filename, 'wt') as outfile:
            outfile.write(json.dumps(obj, indent=2))

    def handle(self, *args, **options):
        da = DeviantArt(settings.DA_CLIENT_ID, settings.DA_CLIENT_SECRET)
        da_username = settings.DA_USERNAME
        dj_user = User.objects.filter(da_username=da_username).first()
        watchers = da.list_watchers(da_username)
        for w in watchers:
            obj, created = DAUser.objects.update_or_create(
                username=w['user']['username'], defaults={
                    "user": dj_user,
                    "userid": w['user'].get('userid')
                })
            profile = da.get_profile(da_username)
            if profile:
                obj.pageview_count = profile['stats']['profile_pageviews']
                obj.deviations_count = profile['stats']['user_deviations']
                obj.watchers_count = profile['user']['stats']['watchers']
                # self.__savejson(profile, "./responses/profile.json")
                obj.save()
