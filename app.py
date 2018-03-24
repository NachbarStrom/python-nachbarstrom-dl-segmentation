import json

from flask import Flask, request
from flask_cors import CORS

from algorithm import get_roofs_information

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def handle_roofs_information_request():
    roof_locations = request.get_json()
    roofs_information = get_roofs_information(roof_locations)
    return json.dumps(roofs_information)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
