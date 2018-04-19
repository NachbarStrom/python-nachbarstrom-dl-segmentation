import pytest
from PIL.Image import Image

from .. import RoofPolygonExtractor, MockRoofPolygonExtractor

valid_location = {"lat": "1.0", "lon": "1.0"}
valid_image = Image()


@pytest.fixture
def extractor():
    return MockRoofPolygonExtractor()


def test_api_with_valid_input(extractor: RoofPolygonExtractor):
    extractor.extract_from(valid_image, valid_location)


def test_validation_rejects_invalid_image(extractor: RoofPolygonExtractor):
    invalid_image = None
    with pytest.raises(AssertionError):
        extractor.extract_from(invalid_image, valid_location)


def test_validation_rejects_invalid_location(extractor: RoofPolygonExtractor):
    invalid_location = {"not": "valid"}
    with pytest.raises(AssertionError):
        extractor.extract_from(valid_image, invalid_location)
