from nachbarstrom.commons.world import Location, Roof, RoofType, RoofOrientation


class RoofProvider:

    def get_roof(self, center_location: Location) -> Roof:
        raise NotImplementedError

    def update(self) -> None:
        raise NotImplementedError

    @staticmethod
    def _validate_input(center_location: Location):
        assert isinstance(center_location, Location)

    @staticmethod
    def _validate_response(roof: Roof):
        assert isinstance(roof, Roof)


class MockRoofProvider(RoofProvider):

    def get_roof(self, center_location: Location) -> Roof:
        self._validate_input(center_location)
        roofs_information = Roof(RoofType.FLAT, RoofOrientation.SOUTH, 1.0)
        self._validate_response(roofs_information)
        return roofs_information

    def update(self) -> None:
        pass
