import pytest
import requests


def roof_polygons_as_expected(roof_polygons):
    assert roof_polygons["type"] == "FeatureCollection"
    features = roof_polygons["features"]
    assert isinstance(features, list)
    for feature in features:
        assert feature["geometry"]["type"] == "LineString"
    return True


@pytest.mark.integration
def test_get_roofs_polygons():
    url = "http://localhost/roofs-polygons"
    center_coordinates = {"lat": "48.1830097", "lon": "11.6099888"}
    response = requests.post(
        url=url,
        json=center_coordinates
    )
    roof_polygons = response.json()

    assert roof_polygons_as_expected(roof_polygons)
