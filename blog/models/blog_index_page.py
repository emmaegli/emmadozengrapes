from django.db import models
from django import forms
from django.conf import settings

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from .blog_page import BlogPage


class BlogIndexPage(Page):

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_context(self, request):
        context = super().get_context(request)

        # Get blog entries
        blog_entries = BlogPage.objects.child_of(self).live()

        # Filter by tag
        tag = request.GET.get("tag")
        if tag:
            blog_entries = blog_entries.filter(tags__name=tag)

        context["blog_entries"] = blog_entries.order_by("-date")
        return context
