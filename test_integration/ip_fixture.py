import pytest


@pytest.fixture
def api_url(request):
    url = request.config.getoption("url")
    return url if url else "http://localhost"
