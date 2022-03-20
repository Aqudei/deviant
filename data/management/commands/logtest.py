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


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        logger.info("YES!")
