from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PluginApp(AppConfig):
    name = "pretalx_orcid"
    verbose_name = "ORCID integration"
    questions = [
        {"setting": "organisation", "question": _("Organisation"), "is_public": True,},
        {"setting": "given_name", "question": _("Given name"), "is_public": False,},
        {"setting": "family_name", "question": _("Family name"), "is_public": False,},
        {"setting": "title", "question": _("Title"), "is_public": False,},
    ]

    class PretalxPluginMeta:
        name = _("ORCID integration")
        author = "Tobias Kunze"
        description = _("Gather speaker data from ORCID")
        visible = True
        version = "0.0.3"

    def ready(self):
        from . import signals  # NOQA

    def installed(self, event):
        from pretalx.cfp.flow import i18n_string
        from pretalx.submission.models import Question

        for question_data in self.questions:
            question = None
            pk = event.settings.get(f"orcid_question_{question_data['setting']}")
            if pk:
                question = Question.all_objects.filter(pk=pk, event=event).first()
            if not question:
                question = Question(
                    event=event,
                    target="speaker",
                    question=i18n_string(question_data["question"], event.locales),
                )
            question.is_public = question_data["is_public"]
            question.active = True
            question.save()
            event.settings.set(
                f"orcid_question_{question_data['setting']}", question.pk
            )

    def uninstalled(self, event):
        from pretalx.submission.models import Question

        for question_data in self.questions:
            question = None
            pk = event.settings.get(f"orcid_question_{question_data['setting']}")
            if pk:
                question = Question.all_objects.filter(pk=pk, event=event).first()
            if question:
                question.active = False
                question.save()


default_app_config = "pretalx_orcid.PluginApp"
