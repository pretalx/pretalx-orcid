from django.db import models
from django.utils.translation import ugettext_lazy as _


class OrcidProfile(models.Model):
    user = models.OneToOneField(
        to="person.User", related_name="orcid_profile", on_delete=models.CASCADE
    )
    orcid = models.CharField(
        null=True, blank=True, verbose_name=_("ORCID"), max_length=40
    )

    access_token = models.CharField(null=True, blank=True, max_length=40)
    refresh_token = models.CharField(null=True, blank=True, max_length=40)
    scope = models.CharField(null=True, blank=True, max_length=40)
    expires_in = models.CharField(null=True, blank=True, max_length=20)
