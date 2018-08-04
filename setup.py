from setuptools import setup

setup(
    name="nachbarstrom-inference",
    version="1.0",
    packages=[
        "nachbarstrom.inference.file_updater",
        "nachbarstrom.inference.geojson_area_calculator",
        "nachbarstrom.inference.roof_provider",
        "nachbarstrom.inference.pv_solar_benefits",
        "nachbarstrom.inference.web_server",
    ],
)
