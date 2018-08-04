import requests

from nachbarstrom.inference.geojson_area_calculator import GeoJsonAreaCalculator

if __name__ == '__main__':
    url = "http://nachbarstrom-backend.northeurope.cloudapp.azure.com" \
          ":3000" \
          "/roofs-polygons"
    json = {"lat": 48.182427, "lon": 11.610666}
    response = requests.post(url, json=json)
    areas = GeoJsonAreaCalculator().get_areas(response.json())
