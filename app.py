import argparse
import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from nachbarstrom.roof_polygon_provider import MockRoofPolygonProvider
from nachbarstrom.roof_provider import MockRoofProvider, TensorFlowRoofProvider
from nachbarstrom.image_provider import MockImageProvider, GoogleImageProvider
from nachbarstrom.file_updater import AsyncFileUpdater, GoogleStorageFileUpdater
from pv_solar_benefits import get_pv_solar_benefits
from nachbarstrom.roof_polygon_extractor import MockRoofPolygonExtractor
from nachbarstrom.world import Location

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


ROOF_POLYGON_EXTRACTOR = MockRoofPolygonExtractor()
IMAGE_PROVIDER = MockImageProvider() if ARGS.develop else GoogleImageProvider()
ROOF_PROVIDER = get_roof_provider()
ROOF_POLYGON_PROVIDER = MockRoofPolygonProvider()
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


@app.route("/roofs-polygons", methods=["POST"])
def get_roofs_polygons():
    center_coords = request.get_json()
    location = Location.from_dict(center_coords)
    roof_polygons = ROOF_POLYGON_PROVIDER.get_nearby_roof_polygons(location, 50)
    return jsonify(roof_polygons)


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
