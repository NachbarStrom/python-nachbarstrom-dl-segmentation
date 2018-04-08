from typing import Dict

from algorithm import Model


class MockModel(Model):

    def get_roofs_information(self, roof_locations: Dict) -> Dict:
        return {
            "data": [
                {
                    "roofType": "some",
                    "orientation": "some",
                    "area": "some"
                }
            ]
        }

    def update(self) -> None:
        pass
