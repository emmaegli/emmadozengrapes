from django.db import models
from django import forms

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.search import index
from modelcluster.fields import ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from blog.blocks import TwoImageBlock, ImageCaptionBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .blog_tag import BlogPageTag


class BlogPage(Page):

    author = models.CharField("Author", max_length=150)

    date = models.DateField("Post date")

    body = StreamField(
        [
            ("title", blocks.CharBlock(classname="blog-title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("image_w_caption", ImageCaptionBlock()),
            ("two_images", TwoImageBlock()),
        ]
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    def blog_preview(self):
        for block in self.body:
            if block.block_type == "paragraph":
                return block.value
        else:
            return "No Preview for this blog"

    def preview_image(self):
        for block in self.body:
            # IF we have a block that is the image type
            if block.block_type == "image":
                return block.value
            # If we have a block that is an image with a caption
            elif block.block_type == "image_w_caption":
                return block.value["image"]
            # If we have a two image block
            elif block.block_type == "two_images":
                # Get the left image stream block
                left_image = block.value["left_image"]
                # If the first image (because there should only ever be one)
                # in the left image is an image block
                if left_image[0].block_type == "image":
                    return left_image[0].value
                # If the first image (because there should only ever be one)
                # in the left image is an image block with a caption, grap the image
                return left_image[0].value["image"]
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("author"),
        index.SearchField("body"),
        index.RelatedFields(
            "tags",
            [
                index.RelatedFields(
                    "tag", [index.SearchField("name", partial_match=True, boost=10)],
                )
            ],
        ),
        index.RelatedFields("categories", [index.SearchField("name"),]),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("author"),
                FieldPanel("date"),
                FieldPanel("tags"),
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Blog information",
        ),
        StreamFieldPanel("body"),
    ]

