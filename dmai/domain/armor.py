from dmai.utils.loader import Loader


class Armor:

    # class variables
    armor_data = dict()

    def __init__(self, armor: str) -> None:
        """Armor class"""
        self.armor = armor
        self.body = None
        self.shield = None
        self._load_armor_data()

        # assign armor to slots on body
        for armor_id in self.armor:
            self.equip_armor(armor_id, self.armor_data[armor_id]["slot"])

    def __repr__(self) -> str:
        return "Armor:\n{a}".format(a=self.armor)

    @classmethod
    def _load_armor_data(cls) -> None:
        """Set the cls.armor_data class variable data"""
        cls.armor_data = Loader.load_json("data/domain/armor.json")

    def equip_armor(self, armor_id: str, slot: str) -> None:
        """Method to equip specified armor to specified slot"""
        if armor_id in self.armor_data:
            self.__setattr__(slot, armor_id)

    def unequip_armor(self, armor_id: str) -> None:
        """Method to unequip specified armor"""
        if self.body == armor_id:
            self.body = None
        elif self.shield == armor_id:
            self.shield = None

    def get_equipped(self, slot) -> dict:
        """Method to get equipped armor.
        Returns a dictionary"""
        if slot == "body":
            return self.armor_data[self.body]
        if slot == "shield":
            return self.armor_data[self.shield]

    def calculate_armor_class(self, dex: int) -> int:
        """Method to calculate the armor class given a dexterity modifier"""
        ac = 10
        if not self.body and not self.shield:
            return ac + dex

        if self.body:
            body = self.get_equipped("body")
            ac = body["ac"]["base"]
            if body["ac"]["mod"] == "dex":
                ac += max(dex, body["ac"]["mod_max"])
                ac += body["ac"]["bonus"]

        if self.shield:
            shield = self.get_equipped("shield")
            ac += shield["ac"]["bonus"]

        return ac
