from typing import Dict
from urllib import request
from io import BytesIO
from PIL import Image

from algorithm.image_provider import ImageProvider


class GoogleImageProvider(ImageProvider):
    """Not thread-safe"""

    def __init__(self, zoom: int=18):
        assert isinstance(zoom, int)
        api_key = "AIzaSyBV6-jGq4ciojBHuKZJ7CZryniRKxJTlFE"
        self._zoom = zoom
        self._image = None
        self._request_url = "https://maps.googleapis.com/maps/api/staticmap?" \
                            "maptype=satellite&center=%s,%s" \
                            "&zoom=" + str(zoom) + \
                            "&size=400x400" \
                            "&key=" + api_key

    def image_from(self, center_coors: Dict) -> Image.Image:
        self._validate_input_format(center_coors)
        self._get_image(center_coors)
        self._validate_output_format(self._image)
        return self._image

    def _get_image(self, center_coors):
        url = self._fill_url(center_coors)
        buffer = BytesIO(request.urlopen(url).read())
        self._image = Image.open(buffer)

    def _fill_url(self, center_coors):
        lat, lon = center_coors["lat"], center_coors["lon"]
        url = self._request_url % (lat, lon)
        return url
