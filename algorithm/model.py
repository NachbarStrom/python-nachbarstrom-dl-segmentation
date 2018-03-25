from typing import Dict
from keras import backend as K
from importlib import reload
from keras.models import load_model
import os
from algorithm.getSatImage import satImgDownload 
import cv2
import numpy as np

ROOF_TYPE_MODEL_PATH = "model/roof_type_model.h5"
ROOF_ORIENTATION_MODEL_PATH = "model/roof_orientation_model.h5"
ROOF_AREA_MODEL_PATH = "model/roof_area_model.h5"

roof_type_classes = ["Flat", "Gabled", "HalfHipped", "Hipped", "Mansard", "Pyramid", "Round"]
orientation_classes = ["East", "East/South", "South", "South/West", "West"]

class Model:
    def __init__(self):
        self._set_keras_backend("tensorflow")
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
            
            roof_type_class = np.argmax(max(self._roof_type_model.predict(X)))
            roof_type = roof_type_classes[roof_type_class]
            
            roof_orientation_class = np.argmax(max(self._roof_orientation_model.predict(X)))
            orientation = orientation_classes[roof_orientation_class]
            
            area_prediction = self._roof_area_model.predict(X)
            area = str(max(max(area_prediction)))
            #area = "20.0"
            
            roof_properties["data"].append({
                "roofType": roof_type,
                "orientation": orientation,
                "area": area
            })

        return roof_properties

    def _load_roof_type_model(self):
        return load_model(ROOF_TYPE_MODEL_PATH)

    def _load_roof_orientation_model(self):
        return load_model(ROOF_ORIENTATION_MODEL_PATH)

    def _load_roof_area_model(self):
        return load_model(ROOF_AREA_MODEL_PATH)

    def _transform_coords_to_X(self, lat_coord, lon_coord):
        satImgDownload(lat_coord, lon_coord)
        img = cv2.imread("currentLocation.png")
        img = cv2.resize(img, (299,299))
        return img[np.newaxis,:,:,:]
    
    def _set_keras_backend(backend):
        if K.backend() != backend:
            os.environ['KERAS_BACKEND'] = backend
            reload(K)
            assert K.backend() == backend


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
