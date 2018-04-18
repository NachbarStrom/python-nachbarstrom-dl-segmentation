from typing import Dict

import numpy as np


class RoofPolygonExtractor:

    def extract_from(self, image: np.ndarray, center_coors: Dict) -> Dict:
        """
        Extract a list of polygons. Each polygon delimits a roof in the
        input image. Input 'center_coors' is the coordinates at the
        center of the image.
        :param image: Image in 3-channel matrix format.
        :param center_coors: Example: { "lat": "1.2", "lon": "1.0" }
        :return: A json-dictionary like 'example_output.py'
        """
        raise NotImplementedError

    @staticmethod
    def _validate_input(image, center_coors):
        """Subclasses can validate the input before processing it."""
        assert "lat" in center_coors and "lon" in center_coors
        assert isinstance(image, np.ndarray)
        assert len(image.shape) == 3

    def _validate_output(self, output: Dict):
        """Subclasses can validate the input before returning it."""
        assert "roofPolygons" in output
        self._validate_polygons(output["roofPolygons"])

    def _validate_polygons(self, roof_polygons):
        assert isinstance(roof_polygons, list)
        for polygon in roof_polygons:
            assert "vertices" in polygon
            self._validate_vertices(polygon["vertices"])

    @staticmethod
    def _validate_vertices(vertices):
        assert isinstance(vertices, list)
        for vertex in vertices:
            assert "lat" in vertex and "lon" in vertex
