from celery import shared_task
from deviant import DeviantArt

@shared_task
def fetch_deviations():
    """
    docstring
    """
    da = DeviantArt()
