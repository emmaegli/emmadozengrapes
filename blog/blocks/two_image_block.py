from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .image_caption_block import ImageCaptionBlock


class TwoImageBlock(blocks.StructBlock):

    left_image = blocks.StreamBlock(
        [("image", ImageChooserBlock()), ("image_w_caption", ImageCaptionBlock())]
    )

    right_image = blocks.StreamBlock(
        [("image", ImageChooserBlock()), ("image_w_caption", ImageCaptionBlock())]
    )

    class Meta:
        template = "blog/blocks/two_image_block.html"
        icon = "placeholder"
        label = "Two Images"

