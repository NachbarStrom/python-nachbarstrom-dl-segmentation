from typing import Sequence, List

from world import Location, Roof, RoofType, RoofOrientation


class Model:

    def get_roofs_information(
            self, roof_locations: Sequence[Location]) -> List[Roof]:
        """
        This function takes a Dict with the location of several roofs
        and returns a Dict with the corresponding roof information for every
        roof.
        :param roof_locations: The roof locations
        :return: Roof information for every roof location
        """
        raise NotImplementedError

    def update(self) -> None:
        raise NotImplementedError

    @staticmethod
    def _validate_input(roof_locations: Sequence[Location]):
        assert isinstance(roof_locations, list)
        for location in roof_locations:
            assert isinstance(location, Location)

    @staticmethod
    def _validate_response(roofs_information: Sequence[Roof]):
        assert isinstance(roofs_information, list)
        for roof in roofs_information:
            assert isinstance(roof, Roof)


class MockModel(Model):

    def get_roofs_information(
            self, roof_locations: Sequence[Location]) -> List[Roof]:
        self._validate_input(roof_locations)
        roofs_information = [Roof(RoofType.FLAT, RoofOrientation.SOUTH, 1.0)]
        self._validate_response(roofs_information)
        return roofs_information

    def update(self) -> None:
        pass
