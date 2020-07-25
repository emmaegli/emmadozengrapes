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

        recent_wine_review = (
            BlogPage.objects.filter(categories__name="Wine Reviews")
            .live()
            .reverse()
            .first()
        )
        context["recent_wine_review"] = recent_wine_review
        recent_blog_posts = BlogPage.objects.order_by("-id").live()
        if recent_wine_review:
            recent_blog_posts = recent_blog_posts.exclude(id=recent_wine_review.id)

        context["recent_blog_posts"] = recent_blog_posts[:2]

        return context
