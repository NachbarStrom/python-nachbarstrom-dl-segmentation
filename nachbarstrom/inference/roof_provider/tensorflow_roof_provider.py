import os

from lazy_import import lazy_module, lazy_callable
import numpy as np
from importlib import reload

from nachbarstrom.commons.image_provider import ImageProvider
from nachbarstrom.commons.world import Location, Roof, RoofType, RoofOrientation
from nachbarstrom.inference.file_updater import FileUpdater
from . import RoofProvider

# Keras with Tensorflow backend takes a long time to load, so we use a
# lighter model for development and load Keras lazily.
backend = lazy_module("keras.backend")
load_model = lazy_callable("keras.models.load_model")

ROOF_TYPE_MODEL = "roof_type_model.h5"
ROOF_ORIENTATION_MODEL = "roof_orientation_model.h5"
ROOF_AREA_MODEL = "roof_area_model.h5"
MODELS_FOLDER = "model"


class TensorFlowRoofProvider(RoofProvider):

    _IMAGE_SIZE = (299, 299)
    _MODEL_NAMES = [
        ROOF_AREA_MODEL,
        ROOF_ORIENTATION_MODEL,
        ROOF_TYPE_MODEL
    ]

    def __init__(self, model_updater: FileUpdater,
                 image_provider: ImageProvider) -> None:
        self._set_tensorflow_backend()
        self._image_provider = image_provider
        self._model_updater = model_updater
        self._update_models_sequentially()

        self._roof_type_model = self._load_model(ROOF_TYPE_MODEL)
        self._roof_orientation_model = self._load_model(ROOF_ORIENTATION_MODEL)
        self._roof_area_model = self._load_model(ROOF_AREA_MODEL)

    def get_roof(self, center_location: Location) -> Roof:
        self._validate_input(center_location)

        pixel_array = self._get_image_of_location_as_pixel_array(center_location)

        roof_type_index = np.argmax(self._roof_type_model.predict(pixel_array))
        roof_type = RoofType(roof_type_index)

        roof_orientation_index = np.argmax(self._roof_orientation_model.predict(pixel_array))
        orientation = RoofOrientation(roof_orientation_index)

        area_prediction = self._roof_area_model.predict(pixel_array)
        print("INFO: Raw area prediction: %f" % area_prediction)

        roof = Roof(roof_type, orientation, area_prediction)
        self._validate_response(roof)
        return roof

    def update(self):
        for model in self._MODEL_NAMES:
            self._model_updater.update_file(model)

    @staticmethod
    def _load_model(model_name):
        file_path = os.path.join(MODELS_FOLDER, model_name)
        return load_model(file_path)

    def _get_image_of_location_as_pixel_array(
            self, location: Location) -> np.ndarray:
        image = self._image_provider.image_from(location)
        image = image.resize(self._IMAGE_SIZE)
        pixel_array = np.array(image.convert("RGB"))
        return pixel_array[np.newaxis, :, :, :]
    
    @staticmethod
    def _set_tensorflow_backend():
        tensorflow = "tensorflow"
        if backend.backend() != tensorflow:
            os.environ['KERAS_BACKEND'] = tensorflow
            reload(backend)
            assert backend.backend() == tensorflow

    def _update_models_sequentially(self):
        for model in self._MODEL_NAMES:
            update_promise = self._model_updater.update_file(model)
            update_promise.wait_until_update_complete()
