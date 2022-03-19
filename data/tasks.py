from asyncio.log import logger
from celery import shared_task
from deviant import DeviantArt
from data import models


@shared_task
def cycle():
    """
    docstring
    """
    for user in models.User.objects.filter(da_username='GrowGetter'):
        da = DeviantArt(user)

        logger.info("Fetching Deviations...")
        for dev in da.list_deviations():
            models.Deviation.objects.update_or_create(
                deviationid=dev['deviationid'], owner=user, defaults={"title": dev['title'], })


        logger.info("Fetching  Favorites...")
        for devobj in models.Deviation.objects.filter(owner=user):
            for fav in da.list_favors(devobj.deviationid):
                user_who_fav = fav['user']
                models.Thank.objects.get_or_create(
                    owner=user, userid=user_who_fav['userid'], username=user_who_fav['username'])


        logger.info("Sending Thanks...")
        for thank in models.Thank.objects.filter(sent=False):
            da.send_thanks(thank.userid)
            thank.sent = True
            thank.save()
