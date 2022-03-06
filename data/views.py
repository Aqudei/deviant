from django.http import HttpResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session
from django.conf import settings
import pickle
from .models import *

# Create your views here.


def index(request):
    """
    docstring
    """
    authorization_url = ''

    if request.method == 'GET':
        return render(request, 'data/index.html')

    if request.method == 'POST':
        scope = 'user browse comment.post'
        deviant = OAuth2Session(settings.DA_CLIENT_ID,
                                redirect_uri=settings.DA_REDIRECT_URL, scope=scope)

        authorization_url, state = deviant.authorization_url(
            settings.DA_AUTHORIZATION_URL)

        return redirect(authorization_url)


def oauth_callback(request):
    """
    docstring
    """

    deviant = OAuth2Session(client_id=settings.DA_CLIENT_ID,
                            redirect_uri=settings.DA_REDIRECT_URL)

    token = deviant.fetch_token(settings.DA_TOKEN_URL,
                                client_secret=settings.DA_CLIENT_SECRET, authorization_response=request.build_absolute_uri())

    response = deviant.get(
        "https://www.deviantart.com/api/v1/oauth2/user/whoami")
    if response.status_code == 200:
        user = response.json()
        User.objects.update_or_create(
            username=user['username'],
            defaults={
                "token": token,
                "da_userid": user['userid'],
                "da_username": user['username']
            }
        )

    return HttpResponse()
