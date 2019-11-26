import json

import requests
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from pretalx.cfp.flow import TemplateFlowStep
from pretalx.common.mixins.views import PermissionRequired

from .forms import OrcidSettingsForm
from .models import OrcidProfile
from .orcid import API_URL, AUTHORIZE_URL, OAUTH_URL, ORCID_URL, get_oauth_url


class OrcidFlowInitial(TemplateFlowStep):
    icon = "info-circle"
    identifier = "orcid_login"
    priority = 15
    template_name = "pretalx_orcid/submission_step.html"

    def get_context_data(self, **kwargs):
        client_id = self.event.settings.orcid_client_id.strip()
        url = get_oauth_url(self.event)
        result = super().get_context_data(**kwargs)
        result["orcid_url"] = (
            AUTHORIZE_URL
            + f"?client_id={client_id}&response_type=code&scope=/authenticate&redirect_uri={url}"
        )
        return result

    def post(self, request):
        request.session["orcid_active"] = None
        next_url = self.get_next_url(request)
        return redirect(next_url) if next_url else None

    def get(self, request):
        request.session["orcid_active"] = request.resolver_match.kwargs["tmpid"]
        return super().get(request)

    def is_completed(self, request):
        return True

    def done(self, request):
        self.request = request
        profile = getattr(request.user, "orcid_profile", None) or OrcidProfile.objects.create(user=request.user)
        data = self.cfp_session.get("data", {})
        for key in ("orcid", "access_token", "refresh_token", "scope", "expires_in", "data"):
            value = data.get(f"orcid_{key}")
            if value:
                setattr(profile, key, value)
        print(profile.__dict__)
        profile.save()

    @property
    def label(self):
        return _("ORCID login")


class OrcidSettings(PermissionRequired, FormView):
    form_class = OrcidSettingsForm
    permission_required = "orga.change_settings"
    template_name = "pretalx_orcid/settings.html"

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result["oauth_url"] = get_oauth_url(self.request.event)
        return result

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.error(request, form.errors)
            return super().get(request, *args, **kwargs)
        form.save()
        messages.success(request, _("The ORCID token has been saved."))
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.event

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {"obj": self.request.event, "attribute_name": "settings", **kwargs}


def orcid_oauth(request, event):
    code = request.GET.get("code")
    response = requests.post(
        OAUTH_URL,
        headers={"accept": "application/json"},
        data={
            "client_id": request.event.settings.orcid_client_id.strip(),
            "client_secret": request.event.settings.orcid_client_secret.strip(),
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": get_oauth_url(request.event),
        },
    )
    response.raise_for_status()
    orcid_data = (
        response.json()
    )  # access_token, refresh_token, expires_in, scope, orcid, name
    person_response = requests.get(
        API_URL + "/v2.0/" + orcid_data["orcid"] + "/record",
        headers={"accept": "application/json", "access token": orcid_data["access_token"], "Authorization type": "Bearer"},
    ).json()
    orcid_organisation = None
    employments = (
        person_response.get("activities-summary", {})
        .get("employments", {})
        .get("employment-summary", [])
    )
    if employments:
        current = [e for e in employments if e.get("end-date") is None]
        if current:
            orcid_organisation = current[0].get("organization").get("name")

    request.session.modified = True
    tmpid = request.session["orcid_active"]
    data = request.session["cfp"][tmpid].get("data", {})

    data["orcid_data"] = json.dumps(person_response)
    for key, value in orcid_data.items():
        data[f"orcid_{key}"] = value

    initial = request.session["cfp"][tmpid].get("initial", {})
    user_initial = initial.get("user", {})
    profile_initial = initial.get("profile", {})
    questions_initial = initial.get("questions", {})
    user_initial["register_name"] = orcid_data.get("name")
    profile_initial["name"] = orcid_data.get("name")
    profile_initial["biography"] = (
        person_response.get("person", {}).get("biography", {}).get("value")
    )
    questions_initial[
        f"question_{request.event.settings.orcid_question_organisation}"
    ] = orcid_organisation
    initial["user"] = user_initial
    initial["profile"] = profile_initial
    initial["questions"] = questions_initial
    request.session["cfp"][tmpid]["initial"] = initial
    return redirect(request.event.cfp.urls.submit + tmpid + "/questions/")
