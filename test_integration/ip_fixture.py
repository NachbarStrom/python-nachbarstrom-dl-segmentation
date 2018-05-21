import pytest


@pytest.fixture
def ip_fixture(request):
    ip_passed = request.config.getoption("ip")
    return ip_passed if ip_passed else "localhost"
