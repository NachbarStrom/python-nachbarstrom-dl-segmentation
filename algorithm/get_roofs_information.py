from typing import Dict
from algorithm.cnn import cnn


def get_roofs_information(roof_locations: Dict) -> Dict:
    """
    This function takes a dictionary from the web request and returns
    the roof in
    :param roof_locations: The roof locations
    :return:
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
    """Validates that the input is as expected."""
    assert "data" in roof_locations
    roofs = roof_locations['data']
    assert isinstance(roofs, list)
    for location in roof_locations['data']:
        assert isinstance(location, dict)
        assert "lat" in location
        assert "lon" in location
