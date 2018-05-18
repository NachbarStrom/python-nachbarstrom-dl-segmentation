from itertools import combinations

import pytest
from PIL.Image import Image

from .. import GoogleImageProvider
from world import Location

germany_location = Location(latitude=48.0, longitude=11.0)


@pytest.fixture
def image_provider():
    return GoogleImageProvider()


def test_validation_rejects_invalid_input(image_provider: GoogleImageProvider):
    invalid_inputs = [None, "invalid"]
    for invalid_input in invalid_inputs:
        with pytest.raises(AssertionError):
            image_provider.image_from(invalid_input)


@pytest.mark.integration
def test_output_is_pillow_image(image_provider: GoogleImageProvider):
    image = image_provider.image_from(germany_location)
    assert isinstance(image, Image)


@pytest.mark.integration
def test_multiple_images_are_different(image_provider: GoogleImageProvider):
    images = _fetch_multiple_images(image_provider)
    for image1, image2 in combinations(images, r=2):
        assert image1 != image2


def _fetch_multiple_images(image_provider):
    images = []
    for num in range(5):
        latitude = 48.0 + num
        location = Location(latitude, longitude=11.0)
        image = image_provider.image_from(location)
        images.append(image)
    return images
