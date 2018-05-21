import pytest

from nachbarstrom.world import Location
from .. import RoofPolygonProvider, MockRoofPolygonProvider


@pytest.fixture
def mock_polygon_provider():
    return MockRoofPolygonProvider()


def test_get_nearby_roof_polygons(mock_polygon_provider: RoofPolygonProvider):
    munich_location = Location(latitude=48.182792, longitude=11.6107118)
    mock_polygon_provider.get_nearby_roof_polygons(munich_location)


def test_get_nearby_roof_polygons_rejects_none_input(
        mock_polygon_provider: RoofPolygonProvider):
    with pytest.raises(AssertionError):
        mock_polygon_provider.get_nearby_roof_polygons(None)


def test_get_nearby_roof_polygons_rejects_invalid_input(
        mock_polygon_provider: RoofPolygonProvider):
    invalid_inputs = [
        [], "invalid"
    ]
    for invalid_input in invalid_inputs:
        with pytest.raises(AssertionError):
            mock_polygon_provider.get_nearby_roof_polygons(invalid_input)
