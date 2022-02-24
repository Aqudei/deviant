from django.http import HttpResponse
from django.shortcuts import render
from requests_oauthlib import OAuth2Session
from django.conf import settings
import pickle

# Create your views here.


def oauth_callback(request):
    """
    docstring
    """

    deviant = OAuth2Session(client_id=settings.DA_CLIENT_ID,
                            redirect_uri=settings.DA_REDIRECT_URL)

    token = deviant.fetch_token(settings.DA_TOKEN_URL,
                                client_secret=settings.DA_CLIENT_SECRET, authorization_response=request.build_absolute_uri())

    with open("./creds", 'wb') as outfile:
        pickle.dump(token, outfile)

    return HttpResponse()
