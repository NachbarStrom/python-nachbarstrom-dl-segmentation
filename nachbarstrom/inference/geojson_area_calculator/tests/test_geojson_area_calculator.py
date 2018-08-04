import pytest

from .. import GeoJsonAreaCalculator

id_ = "hello"
valid_input = {
    "features": [
        {
            "id_": id_,
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [11.6105692, 48.1825211],
                        [11.6105319, 48.1823528],
                        [11.6107666, 48.1823296],
                        [11.6108039, 48.182498],
                        [11.610715, 48.1825068],
                        [11.610599, 48.1825182],
                        [11.6105692, 48.1825211]
                    ],
                    [
                        [11.610625, 48.1824489],
                        [11.6107115, 48.1824404],
                        [11.6107004, 48.1823903],
                        [11.6106139, 48.1823988],
                        [11.610625, 48.1824489]
                    ]
                ]
            }
        }

    ]
}


@pytest.fixture
def geojson_area_calculator():
    return GeoJsonAreaCalculator()


def test_correct_formatting(geojson_area_calculator: GeoJsonAreaCalculator):
    expected_area = "297.077"
    response = geojson_area_calculator.get_areas(valid_input)
    for feature_area in response["areas"]:
        if feature_area["id"] == id_:
            assert expected_area == feature_area["area"]


def test_response_contains_units(
        geojson_area_calculator: GeoJsonAreaCalculator):
    response = geojson_area_calculator.get_areas(valid_input)
    unit = response.get("unit")
    assert unit == "m²"


def test_get_areas_rejects_invalid_input(
        geojson_area_calculator: GeoJsonAreaCalculator):
    invalid_inputs = [1, "string", None, {}]
    for invalid_input in invalid_inputs:
        with pytest.raises(AssertionError):
            geojson_area_calculator.get_areas(invalid_input)
