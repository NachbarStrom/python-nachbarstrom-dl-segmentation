import cv2
from typing import Sequence, List
import os

from PIL.Image import Image
from lazy_import import lazy_module, lazy_callable
import numpy as np
from importlib import reload

from algorithm import Model
from algorithm.getSatImage import satImgDownload
from model_updater import ModelUpdater

# Keras with Tensorflow backend takes a long time to load, so we use a
# lighter model for development and load Keras lazily.
from world import Location, Roof, RoofType, RoofOrientation

backend = lazy_module("keras.backend")
load_model = lazy_callable("keras.models.load_model")

ROOF_TYPE_MODEL = "roof_type_model.h5"
ROOF_ORIENTATION_MODEL = "roof_orientation_model.h5"
ROOF_AREA_MODEL = "roof_area_model.h5"
MODELS_FOLDER = "model"


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

    def get_roofs_information(
            self, roof_locations: Sequence[Location]) -> List[Roof]:
        self._validate_input(roof_locations)

        roofs_information = []
        for location in roof_locations:
            
            pixel_array = self._get_image_of_location(location)
            
            roof_type_index = np.argmax(self._roof_type_model.predict(pixel_array))
            roof_type = RoofType(roof_type_index)
            
            roof_orientation_index = np.argmax(self._roof_orientation_model.predict(pixel_array))
            orientation = RoofOrientation(roof_orientation_index)
            
            area_prediction = self._roof_area_model.predict(pixel_array)
            print("INFO: Raw area prediction: %f" % area_prediction)
            area = max(max(area_prediction))

            roof = Roof(roof_type, orientation, area)
            roofs_information.append(roof)

        self._validate_response(roofs_information)
        return roofs_information

    def update(self):
        for model in self._MODEL_NAMES:
            self._model_updater.update_model(model)

    @staticmethod
    def _load_model(model_name):
        file_path = os.path.join(MODELS_FOLDER, model_name)
        return load_model(file_path)

    @staticmethod
    def _get_image_of_location(location: Location) -> Image:
        satImgDownload(location.latitude, location.longitude)
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
