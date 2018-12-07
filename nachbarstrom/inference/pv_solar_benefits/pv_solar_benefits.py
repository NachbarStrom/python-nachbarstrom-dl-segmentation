from typing import Dict
import numpy as np
import urllib.request
import json
import sys

ENERGY_PER_SQUARE_METER = 200
TILT = 35
TILT_RAD = np.radians(TILT)

AVG_ENERGY_PRICE = 0.2916
PV_PRODUCTION_COST = 0.0935

GET_PV_SOLAR_BENEFITS_REQUIRED_PARAMS = {
    "lat",
    "lon",
    "roofType",
    "orientation",
    "area"
}


def get_pv_solar_benefits(roof_information: Dict) -> Dict:
    lat = roof_information["lat"]
    lon = roof_information["lon"]
    roof_type = roof_information["roofType"]
    roof_orientation = roof_information["orientation"]
    roof_area = roof_information["area"]

    # calculate azimuth
    if roof_orientation == "East":
        azimuth = 90
    elif roof_orientation == "East/South":
        azimuth = 135
    elif roof_orientation == "South":
        azimuth = 180
    elif roof_orientation == "South/West":
        azimuth = 225
    else:
        azimuth = 270

    # calculate suitable roof area
    if roof_type == "Flat":
        size = float(roof_area)
    elif roof_type == "Gabled":
        size = 0.5 * float(roof_area) / np.cos(TILT_RAD)
    elif roof_type == "HalfHipped":
        size = 0.8 * 0.5 * float(roof_area) / np.cos(TILT_RAD)
    elif roof_type == "Hipped":
        size = 0.6 * 0.5 * float(roof_area) / np.cos(TILT_RAD)
    elif roof_type == "Mansard":
        size = (0.5 + 0.2 / np.cos(TILT_RAD)) * float(roof_area)
    elif roof_type == "Pyramid":
        size = 0.4 * float(roof_area) / np.cos(TILT_RAD)
    else:
        size = 0.3 * float(roof_area) / np.cos(TILT_RAD)

    system_capacity = ENERGY_PER_SQUARE_METER * size / 1000.0
    url = "https://developer.nrel.gov/api/pvwatts/v5.json?api_key=q8VOaHxmP5GTjliWsOuyC6KLoU7f0SI6wYDBxvPt&lat=%s&lon=%s&system_capacity=%.2f&azimuth=%s&tilt=%s&array_type=1&module_type=1&losses=10&dataset=intl" % (
    int(lat), int(lon), round(system_capacity, 2), azimuth, TILT)

    try:
        with urllib.request.urlopen(url) as pv_url:
            data = json.loads(pv_url.read().decode())

            output = data["outputs"]
            annualProduction = "%.2f" % round(output["ac_annual"], 2)
            systemCapacity = "%.2f" % round(system_capacity, 2)

            savings = output["ac_annual"] * (AVG_ENERGY_PRICE - PV_PRODUCTION_COST)
            savings = "%.2f" % round(savings, 2)

            solar_benefits = {
                "systemCapacity": systemCapacity,
                "annualProductionInKWhac": annualProduction,
                "savingsInEur": savings
            }
    except:  # catch *all* exceptions
        e = sys.exc_info()[0]
        print("<p>Error: %s</p>" % e)
        solar_benefits = {
            "systemCapacity": "no data available",
            "annualProductionInKWhac": "no data available",
            "savingsInEur": "no data available"
        }

    return solar_benefits
