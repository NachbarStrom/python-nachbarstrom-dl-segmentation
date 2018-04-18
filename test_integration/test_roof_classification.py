import json

import pytest as pytest
import requests


@pytest.mark.integration
def test_running_server_roof_classification():
    global payload_roof_prop
    roof_properties_url = "http://localhost/roof-properties"
    data = {
        "data": [
            {"lat": 10.0, "lon": 2.0}
        ]
    }
    # Test - roof properties
    response_roof_prop = requests.post(url=roof_properties_url, json=data)
    assert response_roof_prop.status_code == 200
    payload_roof_prop = response_roof_prop.json()
    assert "data" in payload_roof_prop
    roofs = payload_roof_prop["data"]
    assert isinstance(roofs, list)
    for roof in roofs:
        assert "roofType" in roof
        assert "orientation" in roof
        assert "area" in roof
