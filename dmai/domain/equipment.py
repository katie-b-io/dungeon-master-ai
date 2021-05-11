from dmai.utils.loader import Loader


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
    def _load_equipment_data(cls) -> None:
        """Set the cls.equipment_data class variable data"""
        cls.equipment_data = Loader.load_json("data/domain/equipment.json")
