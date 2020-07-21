from django.db import models
from django import forms

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
)
from wagtail.search import index
from blog.blocks import TwoImageBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

# Create your models here.


class AboutPage(Page):

    timestamp = models.DateField("Date Last Updated")

    body = StreamField(
        [
            ("title", blocks.CharBlock(classname="about-title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("two_images", TwoImageBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("timestamp"),
        StreamFieldPanel("body"),
    ]
