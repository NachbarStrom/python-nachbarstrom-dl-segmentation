from typing import Dict


def get_pv_solar_benefits(roof_information: Dict) -> Dict:
    validate_input(roof_information)
    return {
        "data": {
            "annualProduction": "1.0",
            "systemCapacity": "1.0",
            "savings": "2.0"
        }
    }


def validate_input(roof_information: Dict):
    assert "data" in roof_information
    roof = roof_information["data"]
    assert "lat" in roof
    assert "lon" in roof
    assert "roofType" in roof
    assert "orientation" in roof
    assert "area" in roof
