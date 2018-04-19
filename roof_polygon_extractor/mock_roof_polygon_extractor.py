from typing import Dict

import numpy as np

from .roof_polygon_extractor import RoofPolygonExtractor
from .example_output import example


class MockRoofPolygonExtractor(RoofPolygonExtractor):

    def extract_from(self, image: np.ndarray, center_coors: Dict) -> Dict:
        self._validate_input(image, center_coors)
        output = example
        self._validate_output(output)
        return output
