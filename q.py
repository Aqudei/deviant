from typing import Any, List
import deviant
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import patreon
import json
import requests

load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID')
REDIRECT_URL = os.environ.get('DA_REDIRECT_URL')
authorization_base_url = 'https://www.deviantart.com/oauth2/authorize'

PATREON_ACCESS_TOKEN = os.environ.get("PATREON_ACCESS_TOKEN")

# REDIRECT_URL = 'http://143.198.179.20/oauthlogin'

BASE_URL = 'https://www.patreon.com'
HEADERS = {
    "Authorization": f"Bearer {PATREON_ACCESS_TOKEN}"
}


def write_json(fn, obj):
    """
    docstring
    """

    with open(fn, 'wt') as outfile:
        outfile.write(json.dumps(obj, indent=2))


def get_campaigns() -> List[Any]:
    """
    docstring
    """
    url = BASE_URL + "/api/oauth2/v2/campaigns"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return

    data = response.json()['data']
    return data


def get_members(campaign_id):
    """
    docstring
    """
    params = {
        "fields[member]": "full_name,is_follower,last_charge_date,last_charge_status,lifetime_support_cents,currently_entitled_amount_cents,patron_status"
    }
    url = BASE_URL + f"/api/oauth2/v2/campaigns/{campaign_id}/members"
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        return

    data = response.json()['data']
    meta = response.json()['meta']
    for d in data:
        yield d

    next_cursor = meta.get('pagination', {}).get('cursors', {}).get('next', {})
    while next_cursor:
        params['page[cursor]'] = next_cursor
        url = BASE_URL + f"/api/oauth2/v2/campaigns/{campaign_id}/members"
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()['data']
        meta = response.json()['meta']

        if response.status_code != 200:
            raise StopIteration

        for d in data:
            yield d

        next_cursor = meta.get('pagination', {}).get(
            'cursors', {}).get('next', {})


def download_members():
    # api_client = patreon.API(PATREON_ACCESS_TOKEN)
    # campaign_response = api_client.fetch_campaign()
    params = {
        'include': 'memberships',
        'fields[member]': 'full_name'
    }
    campaigns = get_campaigns()
    campaign_id = campaigns[0]['id']
    members = get_members(campaign_id)
    body = "["
    for m in members:
        body += json.dumps(m)
        body += ","

    body.strip(",")
    body += "]"

    with open("./responses/members.json", 'wt') as outfile:
        outfile.write(body)


if __name__ == "__main__":
    pass