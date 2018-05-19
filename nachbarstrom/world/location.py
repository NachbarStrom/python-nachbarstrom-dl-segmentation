from typing import Dict


class Location:
    """A location given in latitude and longitude coordinates."""

    def __init__(self, latitude: float, longitude: float):
        assert latitude is not None
        assert longitude is not None
        latitude = float(latitude)
        longitude = float(longitude)

        self._validate_range(latitude, longitude)

        self.longitude = float(longitude)
        self.latitude = float(latitude)

    @staticmethod
    def _validate_range(latitude, longitude):
        # Bounds according to https://goo.gl/EKrCLt
        assert -85.05115 <= latitude <= 85
        assert -180 <= longitude <= 180

    @staticmethod
    def from_dict(coordinates: Dict):
        """
        Returns a Location based on the input dictionary.
        :param coordinates: E.g. {"lat": -1.0, "lon": 1.0}
        :return: A Location instance.
        """
        assert coordinates is not None
        assert "lat" in coordinates
        assert "lon" in coordinates
        return Location(latitude=coordinates["lat"],
                        longitude=coordinates["lon"])

