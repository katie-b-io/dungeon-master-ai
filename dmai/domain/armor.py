from dmai.utils.loader import Loader


class Armor:

    # class variables
    armor_data = dict()

    def __init__(self, armor: str) -> None:
        """Armor class"""
        self.armor = armor
        self._load_armor_data()

    def __repr__(self) -> str:
        return "Armor:\n{a}".format(a=self.armor)

    @classmethod
    def _load_armor_data(cls) -> None:
        """Set the cls.armor_data class variable data"""
        cls.armor_data = Loader.load_json("data/domain/armor.json")
