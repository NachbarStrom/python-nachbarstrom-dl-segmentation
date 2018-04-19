import pytest
import requests


@pytest.mark.integration
def test_running_server_solar_benefits():
    pv_solar_benefits_url = "http://localhost/pv-solar-benefits"
    roof_information = {
        "data": {
            "lat": 48,
            "lon": 12,
            "roofType": "Flat",
            "orientation": "East",
            "area": "20.0"}
    }
    # Test - solar benefits
    response_solar_benefit = requests.post(url=pv_solar_benefits_url,
                                           json=roof_information)
    assert response_solar_benefit.status_code == 200
    payload_solar_benefit = response_solar_benefit.json()
    assert "data" in payload_solar_benefit
    benefits = payload_solar_benefit["data"]
    assert "systemCapacity" in benefits
    assert "annualProduction" in benefits
    assert "savings" in benefits
