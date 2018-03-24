from typing import Dict
from algorithm.cnn import cnn


def get_roofs_information(roof_locations: Dict) -> Dict:
    """
    This function takes a dictionary from the web request and returns
    the roofs information related to

    This function takes a Dict with the location of several roofs
    and returns a Dict with the corresponding roof information for every
    roof.
    :param roof_locations: The roof locations
    :return: Roof information for every roof location
    """
    validate_roof_locations(roof_locations)

    roof_properties = {"data": []}
    for coord in roof_locations["data"]:
        lat_coord = float(coord["lat"])
        lon_coord = float(coord["lon"])
        (roofType, orientation, area) = cnn(lat_coord, lon_coord)
        roof_properties["data"].append({
            "roofType": roofType,
            "orientation": orientation,
            "area": area
        })

    return roof_properties


def validate_roof_locations(roof_locations: Dict) -> None:
    """
    Validates that the input is as expected. Similar to:
    {
        "data": [
            {"lat": 1.0, "lon": 2.0},
            {"lat": 1.0, "lon": 2.0}
        ]
    }
    """
    assert "data" in roof_locations
    roofs = roof_locations['data']
    assert isinstance(roofs, list)
    for location in roof_locations['data']:
        assert isinstance(location, dict)
        assert "lat" in location
        assert "lon" in location
