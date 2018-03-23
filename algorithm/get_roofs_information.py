from typing import Dict


def get_roofs_information(roof_locations: Dict) -> Dict:
    """
    This function takes a dictionary from the web request and returns
    the roof in
    :param roof_locations: The roof locations
    :return:
    """
    validate_roof_locations(roof_locations)

    return {
        "data": [
            {"roof size": "something", "more info": "yay"}
        ]
    }


def validate_roof_locations(roof_locations: Dict) -> None:
    """Validates that the input is as expected."""
    assert "data" in roof_locations
    roofs = roof_locations['data']
    assert isinstance(roofs, list)
    for location in roof_locations['data']:
        assert isinstance(location, dict)
        assert "lat" in location
        assert "lng" in location
