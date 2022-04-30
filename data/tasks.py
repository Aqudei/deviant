import logging
import traceback
from celery import shared_task
from django.conf import settings
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
            models.Thank.objects.update_or_create(
                owner=user, userid=fav.userid, defaults={'username': fav.username})


@shared_task
def cycle_sender():
    """
    docstring
    """

    user = models.User.objects.filter(da_username=settings.DA_USERNAME).first()
    if not user:
        logger.warning("User '{}' cannot be found!".format(
            settings.DA_USERNAME))
        return

    da = DeviantArt(user)

    logger.info("Sending Thanks...")

    thank = models.Thank.objects.filter(owner=user, sent=False).first()
    if not thank:
        return

    try:
        response_json = da.send_message(thank.username, thank.message)
        logger.info(response_json)
    except Exception as e:
        logger.exception(e)
    finally:
        thank.sent = True
        thank.sent_timestamp = timezone.now()
        thank.save()


@shared_task
def cycle_watcher():
    """
    docstring
    """

    dj_user = models.User.objects.filter(
        da_username=settings.DA_USERNAME).first()
    if not dj_user:
        logger.warning("User 'GrowGetter' cannot be found!")
        return

    da = DeviantArt(dj_user)
    for watcher in da.list_watchers(settings.DA_USERNAME):
        watcher_user = watcher['user']
        obj, created = models.DAUser.objects.update_or_create(
            username=watcher_user['username'], user=dj_user, defaults={
                "userid": watcher_user.get('userid')
            })


@shared_task
def cycle_competitor():
    """
    docstring
    """
    user = models.User.objects.filter(da_username='GrowGetter').first()
    if not user:
        logger.info("No user found!")
        return

    mytask, created = models.MyTask.objects.get_or_create(
        name='COMPETITORS', owner=user)

    if mytask.status == 'RUNNING':
        return

    mytask.status = 'RUNNING'
    mytask.save()

    try:
        da = DeviantArt(user, timeout=60)
        competitor = models.Competitor.objects.order_by('updated_at').first()
        profile = da.get_profile(competitor.da_username)
        if not profile:
            logger.info("Profile not found for DA User: {}".format(
                competitor.da_username))
            return
        competitor.da_userid = profile.get(
            'user', {}).get('userid')
        competitor.total_watchers = profile.get(
            'user', {}).get('stats', {}).get('watchers', 0)
        competitor.total_submission = profile.get(
            'stats', {}).get('user_deviations', 0)
        competitor.total_pageviews = profile.get(
            'stats', {}).get('profile_pageviews', 0)
        competitor.save()
    except Exception as e:
        logger.exception(e)
        mytask.last_error = traceback.format_exc()
    finally:
        mytask.last_run = timezone.now()
        mytask.status = 'IDLE'
        mytask.save()


@shared_task
def cycle_competitor_watcher():
    """
    docstring
    """
    user = models.User.objects.filter(da_username='GrowGetter').first()
    if not user:
        logger.info("No user found!")
        return

    mytask, created = models.MyTask.objects.get_or_create(
        name='COMPETITOR_WATCHERS', owner=user)
    if mytask.status == 'RUNNING':
        return

    mytask.status = 'RUNNING'
    mytask.save()

    try:
        competitor = models.Competitor.objects.order_by('updated_at').first()
        if not competitor:
            return

        da = DeviantArt(user, timeout=60)

        watchers = da.list_watchers(competitor.da_username)
        for watcher in watchers:
            logger.info(watcher)
            watcher_obj = models.DAUser.objects.filter(
                username=watcher['user']['username']).first()

            if not watcher_obj:
                continue

            competitor.watchers.add(watcher_obj)
            competitor.save()

    except Exception as e:
        logger.exception(e)
        mytask.last_error = traceback.format_exc()
    finally:
        mytask.last_run = timezone.now()
        mytask.status = 'IDLE'
        mytask.save()
