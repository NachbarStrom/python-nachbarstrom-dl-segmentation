import pytest

from .. import Roof, RoofType, RoofOrientation

valid_roof_type = RoofType.FLAT
valid_roof_orientation = RoofOrientation.SOUTH


def test_constructor_rejects_none_input():
    valid_roof_area = 1.0

    with pytest.raises(AssertionError):
        Roof(None, valid_roof_orientation, valid_roof_area)

    with pytest.raises(AssertionError):
        Roof(valid_roof_type, None, valid_roof_area)

    with pytest.raises(AssertionError):
        Roof(valid_roof_type, valid_roof_orientation, None)


def test_constructor_rejects_negative_area():
    invalid_area = "-1.0"
    with pytest.raises(AssertionError):
        Roof(valid_roof_type, valid_roof_orientation, invalid_area)


def test_constructor_rejects_invalid_area():
    invalid_area = "invalid"
    with pytest.raises(ValueError):
        Roof(valid_roof_type, valid_roof_orientation, invalid_area)


def test_serialize():
    roof = Roof(
        RoofType.FLAT,
        RoofOrientation.SOUTH,
        10.0
    )
    expected_serialized_roof = {
        "roofType": "FLAT",
        "orientation": "SOUTH",
        "area": "10.0"
    }
    assert expected_serialized_roof == roof.serialize()
