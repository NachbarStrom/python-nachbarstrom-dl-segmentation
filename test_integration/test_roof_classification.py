import pytest as pytest
import requests
from .ip_fixture import ip_fixture


@pytest.mark.integration
def test_running_server_roof_classification(ip_fixture):
    roof_properties_url = "http://{ip}/roof-properties".format(ip=ip_fixture)
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
