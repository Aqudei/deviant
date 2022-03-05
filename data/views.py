from django.http import HttpResponse
from django.shortcuts import render
from requests_oauthlib import OAuth2Session
from django.conf import settings
import pickle

# Create your views here.


def index(request):
    """
    docstring
    """
    if request.method == 'GET':
        scope = 'comment.post'
        deviant = OAuth2Session(settings.DA_CLIENT_ID,
                                redirect_uri=settings.DA_REDIRECT_URL, scope=scope)

        authorization_url, state = deviant.authorization_url(
            settings.DA_AUTHORIZATION_URL)

        return render(request, 'data/index.html', {"oauth_url": authorization_url})


def oauth_callback(request):
    """
    docstring
    """

    deviant = OAuth2Session(client_id=settings.DA_CLIENT_ID,
                            redirect_uri=settings.DA_REDIRECT_URL)

    token = deviant.fetch_token(settings.DA_TOKEN_URL,
                                client_secret=settings.DA_CLIENT_SECRET, authorization_response=request.build_absolute_uri())

    print(token)
    with open("./creds", 'wb') as outfile:
        pickle.dump(token, outfile)

    return HttpResponse()
