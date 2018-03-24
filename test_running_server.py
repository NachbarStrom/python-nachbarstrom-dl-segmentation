import json

import requests

local_url = "http://localhost"
data = {
    "data": [
        {"lat": 10.0, "lon": 2.0}
    ]
}
response = requests.post(url=local_url, json=data)

assert response.status_code == 200

payload = json.loads(response.content)
assert "data" in payload
roofs = payload["data"]
assert isinstance(roofs, list)
for roof in roofs:
    assert "roofType" in roof
    assert "orientation" in roof
    assert "area" in roof

print("Test request ran fine: " + str(payload))
