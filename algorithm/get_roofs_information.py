from typing import Dict


class Model:
    def __init__(self):
        self._roof_type_model = self._load_roof_type_model()
        self._roof_orientation_model = self._load_roof_orientation_model()
        self._roof_area_model = self._load_roof_area_model()

    def get_roofs_information(self, roof_locations: Dict) -> Dict:
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
            X = self._transform_coords_to_X(lat_coord, lon_coord)

            roof_type = self._roof_type_model.predict(X)
            orientation = self._roof_orientation_model.predict(X)
            area = self._roof_area_model.predict(X)
            roof_properties["data"].append({
                "roofType": roof_type,
                "orientation": orientation,
                "area": area
            })

        return roof_properties

    def _load_roof_type_model(self):
        pass

    def _load_roof_orientation_model(self):
        pass

    def _load_roof_area_model(self):
        pass

    def _transform_coords_to_X(self, lat_coord, lon_coord):
        pass


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
