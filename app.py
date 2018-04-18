import argparse
import json

import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

from algorithm import MockModel, TensorFlowModel
from model_updater import AsyncModelUpdater, GoogleStorageModelUpdater
from pv_solar_benefits import get_pv_solar_benefits
from roof_polygon_extractor import MockRoofPolygonExtractor

parser = argparse.ArgumentParser()
parser.add_argument("--develop", help="Launches the app in developer mode.",
                    action="store_true")
args = parser.parse_args()


def get_model():
    if args.develop:
        return MockModel()
    else:
        model_updater = AsyncModelUpdater(GoogleStorageModelUpdater())
        return TensorFlowModel(model_updater)


model = get_model()
roof_polygon_extractor = MockRoofPolygonExtractor()
app = Flask(__name__)
CORS(app)


@app.route('/roof-properties', methods=['POST'])
def handle_roofs_information_request():
    roof_locations = request.get_json()
    roofs_information = model.get_roofs_information(roof_locations)
    assert "data" in roofs_information
    return json.dumps(roofs_information)


@app.route("/roofs-polygons", methods=["POST"])
def get_roofs_polygons():
    location = request.get_json()
    image = np.zeros((1, 1, 1))
    roof_polygons = roof_polygon_extractor.extract_from(image, location)
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
