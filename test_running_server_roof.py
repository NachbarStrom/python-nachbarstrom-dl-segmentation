import json

import requests

roof_properties_url = "http://localhost/roof-properties"
pv_solar_benefits_url = "http://localhost/pv-solar-benefits"

data = {
    "data": [
        {"lat": 10.0, "lon": 2.0}
    ]
}

#Test - roof properties
response_roof_prop = requests.post(url=roof_properties_url, json=data)

assert response_roof_prop.status_code == 200

payload_roof_prop = json.loads(response_roof_prop.content)
assert "data" in payload_roof_prop
roofs = payload_roof_prop["data"]
assert isinstance(roofs, list)
for roof in roofs:
    assert "roofType" in roof
    assert "orientation" in roof
    assert "area" in roof
    
print("Test #1 request ran fine: " + str(payload_roof_prop))