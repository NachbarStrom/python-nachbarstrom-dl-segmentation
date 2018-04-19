from itertools import product, combinations

import pytest
from PIL.Image import Image

from ..google_image_provider import GoogleImageProvider

germany_coors = {"lat": 48, "lon": 11}

@pytest.fixture
def image_provider():
    return GoogleImageProvider()


def test_validation_rejects_invalid_input(image_provider: GoogleImageProvider):
    invalid_coordinates = {"not": "valid"}
    with pytest.raises(AssertionError):
        image_provider.image_from(invalid_coordinates)


@pytest.mark.integration
def test_output_is_pillow_image(image_provider: GoogleImageProvider):
    image = image_provider.image_from(germany_coors)
    assert isinstance(image, Image)


@pytest.mark.integration
def test_multiple_images_are_different(image_provider: GoogleImageProvider):
    images = _fetch_multiple_images(image_provider)
    for image1, image2 in combinations(images, r=2):
        assert image1 != image2


def _fetch_multiple_images(image_provider):
    images = []
    for num in range(5):
        coordinates = {"lat": 48 + num, "lon": 11}
        image = image_provider.image_from(coordinates)
        images.append(image)
    return images
