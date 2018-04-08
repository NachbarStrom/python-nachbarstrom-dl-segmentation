from typing import Dict


class Model:

    def get_roofs_information(self, roof_locations: Dict) -> Dict:
        """
        This function takes a Dict with the location of several roofs
        and returns a Dict with the corresponding roof information for every
        roof.
        :param roof_locations: The roof locations
        :return: Roof information for every roof location
        """
        raise NotImplementedError

    def update(self) -> None:
        raise NotImplementedError

    @staticmethod
    def _validate_roof_locations(roof_locations: Dict) -> None:
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
