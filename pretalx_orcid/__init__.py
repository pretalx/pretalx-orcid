from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class PluginApp(AppConfig):
    name = "pretalx_orcid"
    verbose_name = "ORCID integration"

    class PretalxPluginMeta:
        name = gettext_lazy("ORCID integration")
        author = "Tobias Kunze"
        description = gettext_lazy("Gather speaker data from ORCID")
        visible = True
        version = "0.0.0"

    def ready(self):
        from . import signals  # NOQA


default_app_config = "pretalx_orcid.PluginApp"
