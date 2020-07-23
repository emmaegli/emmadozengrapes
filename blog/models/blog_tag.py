from django.db import models

from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )
