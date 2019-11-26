from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PluginApp(AppConfig):
    name = "pretalx_orcid"
    verbose_name = "ORCID integration"

    class PretalxPluginMeta:
        name = _("ORCID integration")
        author = "Tobias Kunze"
        description = _("Gather speaker data from ORCID")
        visible = True
        version = "0.0.2"

    def ready(self):
        from . import signals  # NOQA

    def installed(self, event):
        from pretalx.submission.models import Question

        question = None
        if event.settings.orcid_question_organisation:
            question = Question.all_objects.filter(
                pk=event.settings.orcid_question_organisation, event=event
            ).first()
        if not question:
            question = Question(event=event, target="speaker", question="Organisation",)
        question.is_public = True
        question.active = True
        question.save()
        event.settings.orcid_question_organisation = question.pk

    def uninstalled(self, event):
        from pretalx.submission.models import Question

        if event.settings.orcid_question_organisation:
            question = Question.all_objects.filter(
                pk=event.settings.orcid_question_organisation, event=event
            ).first()
        if question:
            question.active = False
            question.save()


default_app_config = "pretalx_orcid.PluginApp"
