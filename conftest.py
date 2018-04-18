import pytest


def pytest_addoption(parser):
    parser.addoption("--integration", action="store_true",
                     default=False, help="run integration tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        _run_only_integration_tests(items)
    else:
        _run_only_unit_tests(items)


def _run_only_unit_tests(items):
    skip_marker = pytest.mark.skip(reason="need '--integration' option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_marker)


def _run_only_integration_tests(items):
    skip_marker = pytest.mark.skip(reason="running only integration tests.")
    for item in items:
        if "integration" not in item.keywords:
            item.add_marker(skip_marker)
