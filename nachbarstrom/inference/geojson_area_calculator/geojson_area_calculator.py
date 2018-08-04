from area import area


class GeoJsonAreaCalculator:

    def __init__(self, area_func=area):
        self._area_func = area_func

    def get_areas(self, geo_json: dict) -> dict:
        self._validate_input(geo_json)
        feature_areas = [
            self._get_area(feature) for feature in geo_json["features"]
        ]
        return {
            "areas": feature_areas,
            "unit": "m²"
        }

    def _get_area(self, feature):
        geometry_area = self._area_func(feature["geometry"])
        feature_area = {
            "id": feature["id_"],
            "area": self._format_area(geometry_area)
        }
        return feature_area

    @staticmethod
    def _validate_input(geo_json: dict):
        assert isinstance(geo_json, dict)
        features = geo_json.get("features")
        assert isinstance(features, list)
        for feature in features:
            assert "id_" in feature
            assert "geometry" in feature

    @staticmethod
    def _format_area(geometry_area: float):
        return "{:.6}".format(geometry_area)
