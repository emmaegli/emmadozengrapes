from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from wagtail.core.templatetags.wagtailcore_tags import pageurl
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core import mail
from django.template.loader import render_to_string

from blog.models import BlogPage, BlogSubscriber


def send_mass_html_mail(
    datatuple, fail_silently=False, user=None, password=None, connection=None
):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently
    )
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, "text/html")
        messages.append(message)
    return connection.send_messages(messages)


class Command(BaseCommand):
    def handle(self, *args, **options):
        new_blogs = BlogPage.objects.live().filter(
            date__gte=timezone.now() + timezone.timedelta(days=-7)
        )

        # If we have new blogs that we need to update our subscribers about,
        # then send the update email
        if new_blogs.exists():
            to_emails = [str(sub) for sub in BlogSubscriber.objects.all()]
            msg_plain = render_to_string(
                "blog/subscriber_email.txt", {"new_blogs": new_blogs}
            )
            msg_html = render_to_string(
                "blog/subscriber_email.html", {"new_blogs": new_blogs}
            )

            send_mass_html_mail(
                (
                    (
                        "Emma Dozen Grapes Weekly Newsletter",
                        msg_plain,
                        msg_html,
                        None,
                        to_emails,
                    ),
                )
            )
