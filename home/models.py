from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from blog.models import BlogPage


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        recent_wine_reviews = BlogPage.objects.filter(
            categories__name="Wine Reviews"
        ).reverse()[:3]
        context["recent_wine_reviews"] = recent_wine_reviews
        context["recent_blog_posts"] = BlogPage.objects.exclude(
            id__in=recent_wine_reviews.values_list("id", flat=True)
        ).order_by("-id")[:3]

        return context
