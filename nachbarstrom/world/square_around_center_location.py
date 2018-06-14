from math import cos, pi

from .location import Location


class SquareAroundCenterLocation:
    def __init__(self, center: Location, side_length_in_miles: float=0.005):
        assert isinstance(center, Location)
        assert isinstance(side_length_in_miles, float)
        self._center = center
        self._side_length_in_miles = side_length_in_miles
        self._calculate_corner_locations()

    def _calculate_corner_locations(self):
        delta_lat = self._side_length_in_miles / 69
        delta_lon = self._get_delta_lon(delta_lat)

        up = self._center.latitude + delta_lat
        down = self._center.latitude - delta_lat
        right = self._center.longitude + delta_lon
        left = self._center.longitude - delta_lon

        self.bottom_left_location = Location(down, left)
        self.upper_right_location = Location(up, right)

    def _get_delta_lon(self, delta_lat):
        center_lat_in_rad = self._center.latitude / (2 * pi)
        delta_lon = delta_lat / cos(center_lat_in_rad)
        return delta_lon
