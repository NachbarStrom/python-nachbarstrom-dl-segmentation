import pytest


def pytest_addoption(parser):
    parser.addoption("--integration", action="store_true",
                     default=False, help="run integration tests")


def pytest_collection_modifyitems(config, items):
    collected_tests = items
    if config.getoption("--integration"):
        _run_only_integration_tests(collected_tests)
    else:
        _run_only_unit_tests(collected_tests)


def _run_only_unit_tests(collected_tests):
    skip_marker = pytest.mark.skip(reason="need '--integration' option to run")
    for test in collected_tests:
        if "integration" in test.keywords:
            test.add_marker(skip_marker)


def _run_only_integration_tests(collected_tests):
    skip_marker = pytest.mark.skip(reason="running only integration tests.")
    for test in collected_tests:
        if "integration" not in test.keywords:
            test.add_marker(skip_marker)
