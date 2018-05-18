from PIL.Image import Image

from world import Location


class ImageProvider:
    """Provides satellite images."""

    def image_from(self, location: Location) -> Image:
        """
        Get a satellite image.
        :param location: The location at the center of the Image.
        :return: The satellite image in Pillow format.
        """
        raise NotImplementedError

    @staticmethod
    def _validate_input_format(location):
        assert isinstance(location, Location)

    @staticmethod
    def _validate_output_format(image):
        assert isinstance(image, Image)


class MockImageProvider(ImageProvider):
    def image_from(self, location: Location) -> Image:
        self._validate_input_format(location)
        image = Image()
        self._validate_output_format(image)
        return image
