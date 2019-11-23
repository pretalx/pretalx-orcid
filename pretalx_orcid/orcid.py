from django.conf import settings

ORCID_URL = "https://sandbox.orcid.org" if settings.DEBUG else "https://orcid.org"
OAUTH_URL = f"{ORCID_URL}/oauth/token"
AUTHORIZE_URL = f"{ORCID_URL}/oauth/authorize"


def get_oauth_url(event):
    return event.urls.base.full() + "p/orcid/oauth"
