import pytest
import requests

from roof_polygon_extractor import RoofPolygonExtractor


@pytest.mark.integration
def test_get_roofs_polygons():
    url = "http://localhost/roofs-polygons"
    location = {"lat": "1.0", "lon": "1.0"}
    response = requests.post(
        url=url,
        json=location
    )
    output = response.json()
    RoofPolygonExtractor()._validate_output(output)
