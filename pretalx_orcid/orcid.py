from django.conf import settings

ORCID_URL = "https://sandbox.orcid.org" if settings.DEBUG else "https://orcid.org"
API_URL = "https://pub.sandbox.orcid.org" if settings.DEBUG else "https://pub.orcid.org"
OAUTH_URL = f"{ORCID_URL}/oauth/token"
AUTHORIZE_URL = f"{ORCID_URL}/oauth/authorize"


def get_oauth_url(event):
    url = event.urls.base.full() + "p/orcid/oauth"
    if 'localhost/' in url:
        url = url.replace('localhost/', 'localhost:8000/')
    return url
