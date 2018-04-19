from typing import Dict

from PIL.Image import Image

from algorithm.image_provider import ImageProvider


class MockImageProvider(ImageProvider):
    def image_from(self, center_coors: Dict) -> Image:
        self._validate_input_format(center_coors)
        image = Image()
        self._validate_output_format(image)
        return image
