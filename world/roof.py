from enum import Enum


class RoofType(Enum):
    FLAT = 1
    GABLED = 2
    HALF_HIPPED = 3
    HIPPED = 4
    MANSARD = 5
    PYRAMID = 6
    ROUND = 7


class RoofOrientation(Enum):
    EAST = 1
    EAST_SOUTH = 2
    SOUTH = 3
    SOUTH_WEST = 4
    WEST = 5


class Roof:
    def __init__(self, roof_type: RoofType, orientation: RoofOrientation,
                 area: float):
        self._validate_input(roof_type, orientation, area)
        self.type = roof_type
        self.orientation = orientation
        self.area = float(area)

    @staticmethod
    def _validate_input(roof_type, orientation, area):
        assert roof_type is not None
        assert orientation is not None
        assert area is not None
        assert isinstance(roof_type, RoofType)
        assert isinstance(orientation, RoofOrientation)
        area = float(area)
        assert 0 <= area

    def serialize(self):
        return {
            "roofType": self.type.name,
            "orientation": self.orientation.name,
            "area": str(self.area)
        }
