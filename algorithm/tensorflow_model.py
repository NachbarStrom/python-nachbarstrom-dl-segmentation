import cv2
from typing import Dict
import os

from lazy_import import lazy_module, lazy_callable
import numpy as np
from importlib import reload

from algorithm import Model
from algorithm.getSatImage import satImgDownload
from model_updater import ModelUpdater

# Keras with Tensorflow backend takes a long time to load, so we use a
# lighter model for development and load Keras lazily.
backend = lazy_module("keras.backend")
load_model = lazy_callable("keras.models.load_model")

ROOF_TYPE_MODEL = "roof_type_model.h5"
ROOF_ORIENTATION_MODEL = "roof_orientation_model.h5"
ROOF_AREA_MODEL = "roof_area_model.h5"
MODELS_FOLDER = "model"

roof_type_classes = ["Flat", "Gabled", "HalfHipped", "Hipped", "Mansard",
                     "Pyramid", "Round"]
orientation_classes = ["East", "East/South", "South", "South/West", "West"]


class TensorFlowModel(Model):

    _MODEL_NAMES = [
        ROOF_AREA_MODEL,
        ROOF_ORIENTATION_MODEL,
        ROOF_TYPE_MODEL
    ]

    def __init__(self, model_updater: ModelUpdater):
        self._set_tensorflow_backend()
        self._model_updater = model_updater
        self._update_models_sequentially()
        self._roof_type_model = self._load_model(ROOF_TYPE_MODEL)
        self._roof_orientation_model = self._load_model(ROOF_ORIENTATION_MODEL)
        self._roof_area_model = self._load_model(ROOF_AREA_MODEL)

    def get_roofs_information(self, roof_locations: Dict) -> Dict:
        self._validate_roof_locations(roof_locations)

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

            roof_properties["data"].append({
                "roofType": roof_type,
                "orientation": orientation,
                "area": area
            })

        return roof_properties

    def update(self) -> None:
        for model in self._MODEL_NAMES:
            self._model_updater.update_model(model)

    @staticmethod
    def _load_model(model_name):
        file_path = os.path.join(MODELS_FOLDER, model_name)
        return load_model(file_path)

    @staticmethod
    def _transform_coords_to_X(lat_coord, lon_coord):
        satImgDownload(lat_coord, lon_coord)
        img = cv2.imread("currentLocation.png")
        img = cv2.resize(img, (299,299))
        return img[np.newaxis,:,:,:]
    
    @staticmethod
    def _set_tensorflow_backend():
        tensorflow = "tensorflow"
        if backend.backend() != tensorflow:
            os.environ['KERAS_BACKEND'] = tensorflow
            reload(backend)
            assert backend.backend() == tensorflow

    def _update_models_sequentially(self):
        for model in self._MODEL_NAMES:
            update_promise = self._model_updater.update_model(model)
            update_promise.wait_until_update_complete()
