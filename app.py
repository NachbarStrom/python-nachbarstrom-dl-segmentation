import json

from flask import Flask, request
from flask_cors import CORS

from algorithm import Model
from pv_solar_benefits import get_pv_solar_benefits

app = Flask(__name__)
CORS(app)
model = Model()


@app.route('/roof-properties', methods=['POST'])
def handle_roofs_information_request():
    roof_locations = request.get_json()
    roofs_information = model.get_roofs_information(roof_locations)
    assert "data" in roofs_information
    return json.dumps(roofs_information)


@app.route('/pv-solar-benefits', methods=['POST'])
def handle_pv_solar_benefits():
    roof_information = request.get_json()
    solar_benefits = get_pv_solar_benefits(roof_information)
    assert "data" in solar_benefits
    return json.dumps(solar_benefits)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
