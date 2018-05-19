import pytest

from .. import Location


def test_constructor_rejects_invalid_input():
    invalid_input = "invalid"
    valid_input = 1.0

    with pytest.raises(ValueError):
        Location(invalid_input, valid_input)
    with pytest.raises(ValueError):
        Location(valid_input, invalid_input)


def test_constructor_rejects_none_input():
    invalid_input = None
    valid_input = 1.0
    with pytest.raises(AssertionError):
        Location(invalid_input, valid_input)
    with pytest.raises(AssertionError):
        Location(valid_input, invalid_input)


def test_constructor_rejects_out_of_range_latitudes():
    valid_longitude = 1.0
    out_of_range_latitudes = [-86, 86]
    for invalid_latitude in out_of_range_latitudes:
        with pytest.raises(AssertionError):
            Location(invalid_latitude, valid_longitude)


def test_constructor_rejects_out_of_range_longitudes():
    valid_latitude = 1.0
    out_of_range_longitudes = [-181, 181]
    for invalid_longitude in out_of_range_longitudes:
        with pytest.raises(AssertionError):
            Location(valid_latitude, invalid_longitude)


def test_constructor_successful():
    valid_inputs = [1.0, "-1.0"]
    for valid_input in valid_inputs:
        Location(valid_input, valid_input)


def test_from_dict_rejects_invalid_input():
    invalid_dicts = [
        None,
        {},
        {"some": "stuff"},
        {"lat": 1.0},
    ]

    for invalid_dict in invalid_dicts:
        with pytest.raises(AssertionError):
            Location.from_dict(invalid_dict)


def test_from_dict_rejects_invalid_floats():
    invalid_input = {"lat": "invalid", "lon": "invalid"}
    with pytest.raises(ValueError):
        Location.from_dict(invalid_input)


def test_from_dict_successful():
    valid_dicts = [
        {"lat": "1.0", "lon": "1.0"},
        {"lat": -1.0, "lon": -5.0}
    ]
    for valid_dict in valid_dicts:
        Location.from_dict(valid_dict)
