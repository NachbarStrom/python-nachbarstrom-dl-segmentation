import argparse
import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from nachbarstrom.roof_provider import MockRoofProvider, TensorFlowRoofProvider
from nachbarstrom.image_provider import MockImageProvider, GoogleImageProvider
from nachbarstrom.model_updater import AsyncModelUpdater, GoogleStorageModelUpdater
from pv_solar_benefits import get_pv_solar_benefits
from nachbarstrom.roof_polygon_extractor import MockRoofPolygonExtractor
from nachbarstrom.world import Location

parser = argparse.ArgumentParser()
parser.add_argument("--develop", help="Launches the app in developer mode.",
                    action="store_true")
args = parser.parse_args()


def get_model():
    if args.develop:
        return MockRoofProvider()
    else:
        model_updater = AsyncModelUpdater(GoogleStorageModelUpdater())
        return TensorFlowRoofProvider(model_updater)


model = get_model()
roof_polygon_extractor = MockRoofPolygonExtractor()
image_provider = MockImageProvider() if args.develop else GoogleImageProvider()
app = Flask(__name__)
CORS(app)


@app.route('/roof-properties', methods=['POST'])
def handle_roofs_information_request():
    roofs_info = []
    coordinates_list = request.get_json()["data"]
    for coordinates in coordinates_list:
        location = Location.from_dict(coordinates)
        roof = model.get_roof(center_location=location)
        roofs_info.append(roof.serialize())
    return json.dumps({"data": roofs_info})


@app.route("/roofs-polygons", methods=["POST"])
def get_roofs_polygons():
    center_coords = request.get_json()
    location = Location(latitude=center_coords["lat"],
                        longitude=center_coords["lon"])
    image = image_provider.image_from(location)
    roof_polygons = roof_polygon_extractor.extract_from(
        image, center_coords)
    return jsonify(roof_polygons)


@app.route('/pv-solar-benefits', methods=['POST'])
def handle_pv_solar_benefits():
    roof_information = request.get_json()
    solar_benefits = get_pv_solar_benefits(roof_information)
    assert "data" in solar_benefits
    return json.dumps(solar_benefits)


@app.route("/model-change")
def model_changed():
    model.update()
    return "This server acknowledges the model change and will update its " \
           "state."


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
