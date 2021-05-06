from dmai.utils import Loader


class Equipment:

    # class variables
    equipment_data = dict()

    def __init__(self, equipment: str) -> None:
        """Equipment class"""
        self.equipment = equipment
        self._load_equipment_data()

    def __repr__(self) -> str:
        return "Equipment:\n{a}".format(a=self.equipment)

    @classmethod
    def _load_equipment_data(self) -> None:
        """Set the self.equipment_data class variable data"""
        self.equipment_data = Loader.load_json("data/equipment.json")
