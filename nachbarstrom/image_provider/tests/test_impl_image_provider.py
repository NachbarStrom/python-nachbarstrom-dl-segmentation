from itertools import combinations
from typing import Sequence

import pytest
from PIL.Image import Image

from nachbarstrom.image_provider import ImageProvider
from .. import BingImageProvider, GoogleImageProvider
from nachbarstrom.world import Location

germany_location = Location(latitude=48.0, longitude=11.0)


@pytest.fixture
def image_providers():
    return [GoogleImageProvider(), BingImageProvider()]


def test_validation_rejects_invalid_input(
        image_providers: Sequence[ImageProvider]):
    for provider in image_providers:
        invalid_inputs = [None, "invalid"]
        for invalid_input in invalid_inputs:
            with pytest.raises(AssertionError):
                provider.image_from(invalid_input)


@pytest.mark.integration
def test_output_is_pillow_image(image_providers: Sequence[ImageProvider]):
    for provider in image_providers:
        image = provider.image_from(germany_location)
        assert isinstance(image, Image)


@pytest.mark.integration
def test_multiple_images_are_different(image_providers: Sequence[ImageProvider]):
    for provider in image_providers:
        images = _fetch_multiple_images(provider)
        for image1, image2 in combinations(images, r=2):
            assert image1 != image2


def _fetch_multiple_images(provider: ImageProvider):
    images = []
    for num in range(5):
        latitude = 48.0 + num
        location = Location(latitude, longitude=11.0)
        image = provider.image_from(location)
        images.append(image)
    return images
