from django import forms
from django.utils.translation import gettext_lazy as _
from hierarkey.forms import HierarkeyForm


class OrcidSettingsForm(HierarkeyForm):

    orcid_client_id = forms.CharField(required=True, label=_("Client ID"))
    orcid_client_secret = forms.CharField(required=True, label=_("Client Secret"))
