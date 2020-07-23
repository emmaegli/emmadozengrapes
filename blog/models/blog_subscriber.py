from django.db import models
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class BlogSubscriber(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    raw_email = models.EmailField(null=True, blank=True)

    panels = [
        FieldPanel("user"),
        FieldPanel("raw_email"),
    ]

    def send_registration_confirmation(self):
        # msg_plain = render_to_string("templates/blog/subscription_confirmation.txt")
        # msg_html = render_to_string("templates/blog/subscription_confirmation.html",)
        # send_mail(
        #     "emma dozen eggs newsletter subscription confirmation",
        #     msg_plain,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [self.email],
        #     html_message=msg_html,
        # )
        pass

    @property
    def email(self) -> str:
        return self.raw_email if not self.user_id else self.user.email

    def __str__(self):
        return self.email
