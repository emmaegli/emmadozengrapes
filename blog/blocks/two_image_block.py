from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TwoImageBlock(blocks.StructBlock):

    left_image = ImageChooserBlock()

    right_image = ImageChooserBlock()

    class Meta:
        template = "blog/blocks/two_image_block.html"
        icon = "placeholder"
        label = "Two Images"

