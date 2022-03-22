import logging
from celery import shared_task
from deviant import DeviantArt
from data import models

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
                fav_timestimp = fav['time']

                models.Favor.objects.update_or_create(
                    deviation=devobj,
                    userid=user_who_fav['userid'],
                    username=user_who_fav['username'],
                    owner=user,
                    defaults={
                        "fav_timestimp": fav_timestimp
                    }
                )


@shared_task
def cycle_prepmsg(parameter_list):
    """
    docstring
    """
    for user in models.User.objects.filter(da_username='GrowGetter'):
        for fav in models.Favor.objects.filter(owner=user):
            models.Thank.objects.update_or_create(
                owner=user, userid=fav.userid, defaults={'username': fav.username})


@shared_task
def cycle_sender():
    """
    docstring
    """

    for user in models.User.objects.filter(da_username='GrowGetter'):
        for fav in models.Favor.objects.filter(owner=user):
            models.Thank.objects.update_or_create(
                owner=user, userid=fav.userid, defaults={'username': fav.username})

        da = DeviantArt(user)
        logger.info("Sending Thanks...")
        for thank in models.Thank.objects.filter(sent=False):
            da.send_thanks(thank.userid)
            thank.sent = True
            thank.save()
