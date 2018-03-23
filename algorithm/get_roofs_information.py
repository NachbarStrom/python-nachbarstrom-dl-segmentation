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

    roofProperties = {"data":[]}
    for coord in roof_locations["data"]:
        latCoord = float(coord["lat"])
        lonCoord = float(coord["lon"])
        (roofType, orientation, area) = cnn(latCoord, lonCoord)
        roofProperties["data"].append({"roofType":roofType, "orientation":orientation, "area":area})

    return roofProperties


def validate_roof_locations(roof_locations: Dict) -> None:
    """Validates that the input is as expected."""
    assert "data" in roof_locations
    roofs = roof_locations['data']
    assert isinstance(roofs, list)
    for location in roof_locations['data']:
        assert isinstance(location, dict)
        assert "lat" in location
        assert "lon" in location
