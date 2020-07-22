from django.db import models
from django import forms

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from blog.blocks import TwoImageBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        ImageChooserPanel("icon"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "blog categories"


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


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


class BlogPage(Page):

    author = models.CharField("Author", max_length=150)

    date = models.DateField("Post date")

    body = StreamField(
        [
            ("title", blocks.CharBlock(classname="blog-title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
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
            if block.block_type == "image":
                return block.value
            elif block.block_type == "two_images":
                return block.value["left_image"]
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


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(
        BlogPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("caption"),
    ]
