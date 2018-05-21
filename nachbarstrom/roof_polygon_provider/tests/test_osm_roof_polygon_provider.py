import itertools
from unittest.mock import MagicMock

import overpass
import pytest
from geojson import FeatureCollection, Feature, LineString

from nachbarstrom.world import Location
from .. import OSMRoofPolygonProvider

MUNICH_LOCATION = Location(latitude=48.182792, longitude=11.6107118)


def setup_overpass_api_mock():
    overpass_api = MagicMock(spec=overpass.API)
    feature_collection = FeatureCollection([Feature(geometry=LineString())])
    overpass_api.get.return_value = feature_collection
    return overpass_api


@pytest.fixture
def osm_roof_polygon_provider():
    return OSMRoofPolygonProvider(setup_overpass_api_mock())


def test_get_nearby_roof_polygons_calls_api(
        osm_roof_polygon_provider: OSMRoofPolygonProvider):
    osm_roof_polygon_provider.get_nearby_roof_polygons(MUNICH_LOCATION)
    osm_roof_polygon_provider._overpass_api.get.assert_called_once()


def test_nearby_roof_polygons_calls_api_with_same_query(
        osm_roof_polygon_provider: OSMRoofPolygonProvider):
    number_of_calls = 4
    for _ in range(number_of_calls):
        osm_roof_polygon_provider.get_nearby_roof_polygons(MUNICH_LOCATION)

    assert api_called_with_same_query(number_of_calls,
                                      osm_roof_polygon_provider)


def api_called_with_same_query(number_of_calls, osm_roof_polygon_provider):
    queries = osm_roof_polygon_provider._overpass_api.get.call_args_list
    assert number_of_calls == len(queries)
    for query1, query2 in itertools.combinations(queries, 2):
        assert query1 == query2
    return True
