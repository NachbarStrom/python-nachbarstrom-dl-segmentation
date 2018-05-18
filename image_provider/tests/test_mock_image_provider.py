import pytest
from PIL.Image import Image

from .. import MockImageProvider
from world import Location


@pytest.fixture
def mock_image_provider():
    return MockImageProvider()


def test_image_from(mock_image_provider: MockImageProvider):
    location = Location(latitude=0.0, longitude=0.0)
    image = mock_image_provider.image_from(location)
    assert isinstance(image, Image)
