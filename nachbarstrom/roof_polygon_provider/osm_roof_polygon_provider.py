import overpass

from geojson import GeoJSON

from nachbarstrom.world import Location
from . import RoofPolygonProvider


class OSMRoofPolygonProvider(RoofPolygonProvider):

    _VERBOSITY = "geom"
    _QUERY_TEMPLATE = "(" \
                      "rel[building](around:{radius},{lat},{lon});" \
                      "way[building](around:{radius},{lat},{lon});" \
                      ")->.results;" \
                      "(.results;>;);"

    def __init__(self, overpass_api=overpass.API()):
        self._overpass_api = overpass_api

    def get_nearby_roof_polygons(self, center_location: Location,
                                 radius_in_meters: int=30) -> GeoJSON:
        self._validate_input(center_location, radius_in_meters)
        query = self._fill_query(center_location, radius_in_meters)
        roof_polygons = self._overpass_api.get(query, verbosity=self._VERBOSITY)
        self._validate_output(roof_polygons)
        return roof_polygons

    def _fill_query(self, center_location: Location, radius_in_meters: int):
        return self._QUERY_TEMPLATE.format(
            radius=radius_in_meters,
            lat=center_location.latitude,
            lon=center_location.longitude
        )
