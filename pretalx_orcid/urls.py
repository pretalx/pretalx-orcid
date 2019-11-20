from django.conf.urls import url
from pretalx.event.models.event import SLUG_CHARS

from .views import OrcidSettings, orcid_oauth

urlpatterns = [
    # TODO: global url at /p/orcid/authenticate
    #       receives server response, sets data on session (and authed user if available)
    #       retrieves orcid data and sets intial for user/person form
    #       redirects back to cfp based on session data
    # TODO: user URL to update orcid data (laters)
    url(
        fr"^orga/event/(?P<event>[{SLUG_CHARS}]+)/settings/p/orcid/$",
        OrcidSettings.as_view(),
        name="settings",
    ),
    url(fr"^(?P<event>[{SLUG_CHARS}]+)/p/orcid/oauth$", orcid_oauth, name="oauth",),
]
