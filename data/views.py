import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session
from django.conf import settings
import pickle
from data import forms
from .models import *
from rest_framework import decorators, response

# Create your views here.


def install_patreon(request):
    """
    docstring
    """
    scope = 'user browse comment.post'
    deviant = OAuth2Session(settings.DA_CLIENT_ID,
                            redirect_uri=settings.DA_REDIRECT_URL, scope=scope)

    authorization_url, state = deviant.authorization_url(
        settings.DA_AUTHORIZATION_URL)

    return redirect(authorization_url)


decorators.api_view(http_method_names=['post'])


def patreon_hook(request):
    """
    docstring
    """
    secret = 'IundVGCpkwhTRBAOSrTiCsQ-nRkp0fSfgwrR6AXl2nX3n-xqFnTTJ564jkLgnA9u'

    headers = json.dumps(request.headers.__dict__, indent=2)
    HookRequest.objects.create(
        body=json.dumps(request.data, indent=2),
        headers=headers
    )
    
    return response.Response()


def install_da(request):
    """
    docstring
    """

    if request.method == 'POST':
        scope = 'user browse comment.post'
        deviant = OAuth2Session(settings.DA_CLIENT_ID,
                                redirect_uri=settings.DA_REDIRECT_URL, scope=scope)

        authorization_url, state = deviant.authorization_url(
            settings.DA_AUTHORIZATION_URL)

        return redirect(authorization_url)


def index(request):
    """
    docstring
    """
    authorization_url = ''

    if request.method == 'GET':
        return render(request, 'data/index.html')


def init_auth(request):
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
            da_username=user['username'],
            defaults={
                "token": token,
                "da_userid": user['userid'],
            }
        )

    return redirect('/admin/data/user/')


def views(request):
    """
    docstring
    """
    pass


def post2profile(request):
    """
    docstring
    """
    if request.method == 'GET':
        form = forms.MessageForm()
        return render(request, 'data/message.html', {'form': form})

    if request.method == 'POST':
        form = forms.MessageForm(request.POST)
        if not form.is_valid():
            return render(request, 'data/message.html', {'form': form})
        ids = [int(id_) for id_ in request.GET.get('ids').split(',')]
        for da_user in DAUser.objects.filter(id__in=ids):
            Thank.objects.create(
                message=form.cleaned_data['message'],
                owner=request.user,
                userid=da_user.userid,
                username=da_user.username
            )

        return redirect('/admin/data/dauser/')
