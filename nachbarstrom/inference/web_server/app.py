import argparse
import json

from flask import Flask, request
from flask_cors import CORS

from nachbarstrom.inference.roof_provider import MockRoofProvider, TensorFlowRoofProvider
from nachbarstrom.inference.file_updater import AsyncFileUpdater, GoogleStorageFileUpdater
from nachbarstrom.inference.pv_solar_benefits import get_pv_solar_benefits

from nachbarstrom.commons.image_provider import MockImageProvider, GoogleImageProvider
from nachbarstrom.commons.world import Location

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--develop", help="Launches the app in developer mode.",
                    action="store_true")
ARGS = PARSER.parse_args()


def get_roof_provider():
    """Returns either the production or the development RoofProvider. """
    if ARGS.develop:
        return MockRoofProvider()
    else:
        model_updater = AsyncFileUpdater(GoogleStorageFileUpdater())
        return TensorFlowRoofProvider(model_updater, IMAGE_PROVIDER)


IMAGE_PROVIDER = MockImageProvider() if ARGS.develop else GoogleImageProvider()
ROOF_PROVIDER = get_roof_provider()
app = Flask(__name__)
CORS(app)


@app.route('/roof-properties', methods=['POST'])
def handle_roofs_information_request():
    roofs_info = []
    coordinates_list = request.get_json()["data"]
    for coordinates in coordinates_list:
        location = Location.from_dict(coordinates)
        roof = ROOF_PROVIDER.get_roof(center_location=location)
        roofs_info.append(roof.serialize())
    return json.dumps({"data": roofs_info})


@app.route('/pv-solar-benefits', methods=['POST'])
def handle_pv_solar_benefits():
    roof_information = request.get_json()
    solar_benefits = get_pv_solar_benefits(roof_information)
    assert "data" in solar_benefits
    return json.dumps(solar_benefits)


@app.route("/model-change")
def model_changed():
    ROOF_PROVIDER.update()
    return "This server acknowledges the model change and will update its " \
           "state."


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=80,
        threaded=False # Otherwise, Flask+Keras+TensorFlow will blow up
        # See: https://goo.gl/idiCL4
    )
