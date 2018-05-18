from urllib import request
from io import BytesIO
from PIL import Image

from world import Location
from .image_provider import ImageProvider


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

    def image_from(self, location: Location) -> Image.Image:
        self._validate_input_format(location)
        self._get_image(location)
        self._validate_output_format(self._image)
        return self._image

    def _get_image(self, location):
        url = self._fill_url(location)
        buffer = BytesIO(request.urlopen(url).read())
        self._image = Image.open(buffer)

    def _fill_url(self, location: Location):
        return self._request_url % (location.latitude, location.longitude)
