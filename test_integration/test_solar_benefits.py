import pytest
import requests
from .ip_fixture import api_url


@pytest.mark.integration
def test_running_server_solar_benefits(api_url):
    pv_solar_benefits_url = "{api_url}/pv-solar-benefits".format(api_url=api_url)
    roof_information = {
        "lat": 48,
        "lon": 12,
        "roofType": "Flat",
        "orientation": "East",
        "area": "20.0",
    }
    # Test - solar benefits
    response_solar_benefit = requests.post(url=pv_solar_benefits_url,
                                           json=roof_information)
    assert response_solar_benefit.status_code == 200
    benefits = response_solar_benefit.json()
    assert "systemCapacity" in benefits
    assert "annualProductionInKWhac" in benefits
    assert "savingsInEur" in benefits
