from geojson import GeoJSON, FeatureCollection, Feature
from geojson.geometry import LineString

from nachbarstrom.world import Location


class RoofPolygonProvider:

    def get_nearby_roof_polygons(self, center_location: Location,
                                 radius_in_meters: int=30) -> GeoJSON:
        """
        Return the roof polygons with at least one vertex in the circled
        area.
        :param center_location: The center of the area.
        :param radius_in_meters: The radius of the circled area.
        :return: A GeoJSON object with the roof polygons.
        """
        raise NotImplementedError

    @staticmethod
    def _validate_input(location, radius):
        assert location is not None
        assert isinstance(location, Location)

        assert radius is not None
        assert isinstance(int(radius), int)

    @staticmethod
    def _validate_output(geo_json):
        assert geo_json is not None
        assert isinstance(geo_json, GeoJSON)


class MockRoofPolygonProvider(RoofPolygonProvider):

    def get_nearby_roof_polygons(self, center_location: Location,
                                 radius_in_meters: int=30) -> GeoJSON:
        self._validate_input(center_location, radius_in_meters)
        geo_json = FeatureCollection([Feature(geometry=LineString())])
        self._validate_output(geo_json)
        return geo_json
