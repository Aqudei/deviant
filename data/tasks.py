import logging
from celery import shared_task
from deviant import DeviantArt
from data import models
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def cycle_deviations():
    """
    docstring
    """
    for user in models.User.objects.filter(da_username='GrowGetter'):
        da = DeviantArt(user)

        logger.info("Fetching Deviations...")
        for dev in da.list_deviations():
            favourites = dev['stats'].get('favourites', 0)

            models.Deviation.objects.update_or_create(deviationid=dev['deviationid'], owner=user, defaults={
                                                      "title": dev['title'], "favourites": favourites})


@shared_task
def cycle_favorites():
    """
    docstring
    """
    for user in models.User.objects.filter(da_username='GrowGetter'):
        da = DeviantArt(user)

        logger.info("Fetching  Favorites...")
        for devobj in models.Deviation.objects.filter(owner=user):
            for fav in da.list_favors(devobj.deviationid):
                user_who_fav = fav['user']
                fav_timestamp = fav['time']

                models.Favor.objects.update_or_create(
                    deviation=devobj,
                    userid=user_who_fav['userid'],
                    username=user_who_fav['username'],
                    owner=user,
                    defaults={
                        "fav_timestamp": fav_timestamp
                    }
                )


@shared_task
def cycle_prepmsg():
    """
    docstring
    """
    for user in models.User.objects.filter(da_username='GrowGetter'):
        for fav in models.Favor.objects.filter(owner=user):
            models.Thank.objects.get_or_create(
                owner=user, userid=fav.userid, username=fav.username)


@shared_task
def cycle_sender():
    """
    docstring
    """

    user = models.User.objects.filter(da_username='GrowGetter').first()
    if not user:
        logger.warning("User 'GrowGetter' cannot be found!")
        return

    da = DeviantArt(user)
    logger.info("Sending Thanks...")
    for thank in models.Thank.objects.filter(owner=user, sent=False):
        try:
            response_json = da.send_message(thank.username, thank.message)
            logger.info(response_json)
            thank.sent = True
            thank.sent_timestamp = timezone.now()
            thank.save()
        except Exception as e:
            logger.exception(e)


@shared_task
def cycle_watcher():
    """
    docstring
    """

    user = models.User.objects.filter(da_username='GrowGetter').first()
    if not user:
        logger.warning("User 'GrowGetter' cannot be found!")
        return

    da = DeviantArt(user)
    for watcher in da.list_watchers('GrowGetter'):
        watcher_user = watcher['user']


@shared_task
def cycle_competitor():
    """
    docstring
    """
    user = models.User.objects.filter(da_username='GrowGetter').first()
    if not user:
        return

    da = DeviantArt(user, timeout=10)
    for competitor in models.Competitor.objects.all():
        watchers = da.list_watchers(competitor.da_username)
        for watcher in watchers:
            watcher_obj, created = models.DAUser.objects.update_or_create(
                username=watcher['user']['username'], defaults={
                    "userid":  watcher['user']['userid']
                })
            competitor.watchers.add(watcher_obj)
