from dmai.utils.loader import Loader


class Weapons:

    # class variables
    weapons_data = dict()

    def __init__(self, weapons: str, proficiencies=None) -> None:
        """Weapons class"""
        self.weapons = weapons
        self.right_hand = None
        self.left_hand = None
        self.proficiencies = proficiencies
        self._load_weapons_data()

        # equip first weapon
        weapon_id = next(iter(self.weapons))
        weapon_count = self.weapons[weapon_id]

        if weapon_count > 0:
            self.equip_weapon(weapon_id, "right_hand")
        if weapon_count > 1 or self.has_property(weapon_id, "two_handed"):
            # equip the weapon to second hand if able
            self.equip_weapon(weapon_id, "left_hand")

    def __repr__(self) -> str:
        return "Weapons:\n{a}".format(a=self.weapons)

    @classmethod
    def _load_weapons_data(cls) -> None:
        """Set the cls.weapons_data and cls.weapon_properties class variable data"""
        cls.weapons_data = Loader.load_domain("weapons")
        cls.weapon_properties = Loader.load_domain("weapon_properties")

    def get_weapon(self, weapon_id: str) -> bool:
        """Method to return specified weapon"""
        if weapon_id in self.weapons_data:
            return self.weapons_data[weapon_id]

    def is_ranged(self, weapon_id: str) -> bool:
        """Method to determine if the weapon is ranged"""
        if weapon_id in self.weapons_data:
            weapon = self.weapons_data[weapon_id]
            if "ranged" in weapon["type"]:
                return True
        return False

    def has_property(self, weapon_id: str, prop: str) -> bool:
        """Method to determine if weapon has property"""
        if weapon_id in self.weapons_data:
            weapon = self.weapons_data[weapon_id]
            if prop in weapon["properties"]:
                return True
        return False

    def get_damage(self, weapon_id: str) -> str:
        """Method to return the weapon damage"""
        if weapon_id in self.weapons_data:
            damage = self.weapons_data[weapon_id]["damage"]
            return "{t}{d}".format(t=damage["total"], d=damage["die"])

    def get_damage_type(self, weapon_id: str) -> str:
        """Method to return the weapon damage type"""
        if weapon_id in self.weapons_data:
            damage = self.weapons_data[weapon_id]["damage"]
            return damage["type"]

    def equip_weapon(self, weapon_id: str, slot: str) -> None:
        """Method to equip specified weapon"""
        if weapon_id in self.weapons_data:
            self.__setattr__(slot, weapon_id)

    def unequip_weapon(self, weapon_id: str) -> None:
        """Method to unequip specified weapon"""
        if self.right_hand == weapon_id:
            self.right_hand = None
        elif self.left_hand == weapon_id:
            self.left_hand = None

    def get_equipped(self, slot) -> dict:
        """Method to get equipped weapon.
        Returns a dictionary"""
        if slot == "right_hand" and self.right_hand:
            return self.weapons_data[self.right_hand]
        if slot == "left_hand" and self.left_hand:
            return self.weapons_data[self.left_hand]

    def get_all(self) -> list:
        """Method to return all the weapons"""
        return [self.weapons_data[weapon] for weapon in self.weapons]

    def get_proficient(self) -> list:
        """Return the proficient weapons in a list"""
        all_profs = []
        for prof in self.proficiencies:
            if prof in self.weapons_data:
                all_profs.append(self.weapons_data[prof])
            else:
                # proficiency could be type
                for weapon in self.weapons_data.values():
                    if prof in weapon["type"]:
                        all_profs.append(weapon)
        return all_profs