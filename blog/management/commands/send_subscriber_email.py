from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from wagtail.core.templatetags.wagtailcore_tags import pageurl

from blog.models import BlogPage, BlogSubscriber


class Command(BaseCommand):
    def handle(self, *args, **options):
        new_blogs = BlogPage.objects.live().filter(
            date__gte=timezone.now() + timezone.timedelta(days=-7)
        )

        # If we have new blogs that we need to update our subscribers about,
        # then send the update email
        if new_blogs.exists():
            to_emails = [str(sub) for sub in BlogSubscriber.objects.all()]
            print(to_emails)
            print([page.url for page in new_blogs])
