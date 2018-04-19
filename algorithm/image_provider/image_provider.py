from typing import Dict

from PIL.Image import Image


class ImageProvider:
    """Provides satellite images."""

    def image_from(self, center_coors: Dict) -> Image:
        """
        Get a satellite image.
        :param center_coors: The coordinates at the center of the image.
        :return: The satellite image in Pillow format.
        """
        raise NotImplementedError

    @staticmethod
    def _validate_input_format(coordinates):
        assert "lat" in coordinates and "lon" in coordinates

    @staticmethod
    def _validate_output_format(image):
        assert isinstance(image, Image)
