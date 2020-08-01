from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class ImageCaptionBlock(blocks.StructBlock):

    image = ImageChooserBlock()

    caption = blocks.CharBlock(max_length=150)

    class Meta:
        template = "blog/blocks/image_caption_block.html"
        icon = "image"
        label = "Image w/ caption"

