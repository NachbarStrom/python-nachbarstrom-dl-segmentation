import pytest

from nachbarstrom.world import Location
from .. import SquareAroundCenterLocation

invalid_inputs = [None, 1, "string"]
valid_location = Location(1.0, 1.0)


def test_construction_rejects_invalid_input_for_location():
    for invalid_input in invalid_inputs:
        with pytest.raises(AssertionError):
            SquareAroundCenterLocation(center=invalid_input)


def test_construction_rejects_invalid_input_for_side_lenght():
    for invalid_input in invalid_inputs:
        with pytest.raises(AssertionError):
            SquareAroundCenterLocation(valid_location, invalid_input)


def test_object_contains_bottom_left_location():
    square = SquareAroundCenterLocation(valid_location)
    assert isinstance(square.bottom_left_location, Location)


def test_object_contains_upper_right_location():
    square = SquareAroundCenterLocation(valid_location)
    assert isinstance(square.upper_right_location, Location)
