from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from pretalx.cfp.signals import cfp_steps
from pretalx.orga.signals import activate_event, nav_event_settings


@receiver(cfp_steps)
def orcid_cfp_steps(sender, **kwargs):
    from .views import OrcidFlowInitial

    return [OrcidFlowInitial]


@receiver(nav_event_settings)
def orcid_settings(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []
    return [
        {
            "label": "ORCID",
            "url": reverse(
                "plugins:pretalx_orcid:settings", kwargs={"event": request.event.slug},
            ),
            "active": request.resolver_match.url_name == "plugins:orcid:settings",
        }
    ]


@receiver(activate_event)
def orcid_activate_event(sender, request, **kwargs):
    if not request.event.settings.orcid_client_id:
        raise Exception(
            _(
                "Please configure your ORCID access settings or disable the ORCID plugin!"
            )
        )
