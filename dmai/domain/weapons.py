from dmai.utils.loader import Loader
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Weapons:

    # class variables
    weapons_data = dict()

    def __init__(self, weapons: str, state: State, proficiencies=None) -> None:
        """Weapons class"""
        self.weapons = weapons
        self.state = state
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

    def can_equip(self, weapon_id: str) -> tuple:
        """Method to return whether specified weapon can be equipped.
        Returns a tuple with the boolean and a string with a reason."""
        if not weapon_id in self.weapons:
            return (False, "not owned")

        weapon_count = self.weapons[weapon_id]
        right_weapon = self.get_equipped("right_hand")
        left_weapon = self.get_equipped("left_hand")

        if weapon_count == 1 and right_weapon and weapon_id == right_weapon["id"]:
            return (False, "already equipped")

        if weapon_count == 1 and left_weapon and weapon_id == left_weapon["id"]:
            return (False, "already equipped")

        if right_weapon and left_weapon:
            return (False, "no free slots")
        return (True, "")

    def can_unequip(self, weapon_id: str) -> tuple:
        """Method to return whether specified weapon can be unequipped.
        Returns a tuple with the boolean and a string with a reason."""
        if not weapon_id:
            if not self.get_equipped("right_hand") and not self.get_equipped(
                "left_hand"
            ):
                return (False, "nothing equipped")
            else:
                return (True, "")

        if not weapon_id in self.weapons:
            return (False, "not owned")

        if not self.is_equipped(weapon_id):
            return (False, "not equipped")
        return (True, "")

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

    def get_damage_dice(self, weapon_id: str) -> dict:
        """Method to return the weapon damage dice spec"""
        if weapon_id in self.weapons_data:
            return self.weapons_data[weapon_id]["damage"]
        
    def get_damage(self, weapon_id: str) -> str:
        """Method to return the weapon damage"""
        damage = self.get_damage_dice(weapon_id)
        return "{t}{d}".format(t=damage["total"], d=damage["die"])

    def get_damage_type(self, weapon_id: str) -> str:
        """Method to return the weapon damage type"""
        damage = self.get_damage_dice(weapon_id)
        return damage["type"]

    def get_damage_ability(self, weapon_id: str) -> str:
        """Method to return the damage modifier ability"""
        if self.has_property(weapon_id, "finesse"):
            if self.is_ranged(weapon_id):
                return "dex"
            else:
                c = self.state.get_player().character
                if c.get_ability_modifier("dex") > c.get_ability_modifier("str"):
                    return "dex"
        return "str"

    def equip_weapon(self, weapon_id: str, slot: str = None) -> bool:
        """Method to equip specified weapon"""
        if weapon_id in self.weapons:
            if slot:
                self.state.__setattr__(slot, weapon_id)
                return True
            else:
                if self.has_property(weapon_id, "two_handed"):
                    self.state.__setattr__("left_hand", weapon_id)
                    self.state.__setattr__("right_hand", weapon_id)
                    return True
                else:
                    if self.get_equipped("right_hand"):
                        self.state.__setattr__("left_hand", weapon_id)
                        return True
                    self.state.__setattr__("right_hand", weapon_id)
                    return True
        return False

    def unequip_weapon(self, weapon_id: str = None) -> bool:
        """Method to unequip specified weapon"""
        if not weapon_id:
            self.state.right_hand = None
            self.state.left_hand = None
            return True
        if self.has_property(weapon_id, "two_handed"):
            self.state.right_hand = None
            self.state.left_hand = None
            return True
        if self.state.right_hand == weapon_id:
            self.state.right_hand = None
            return True
        if self.state.left_hand == weapon_id:
            self.state.left_hand = None
            return True
        return False

    def get_equipped(self, slot: str = None) -> dict:
        """Method to get equipped weapon.
        Returns a dictionary"""
        if slot == "right_hand" and self.state.right_hand:
            return self.weapons_data[self.state.right_hand]
        if slot == "left_hand" and self.state.left_hand:
            return self.weapons_data[self.state.left_hand]
        if slot == "any":
            if self.state.right_hand:
                return self.weapons_data[self.state.right_hand]
            elif self.state.left_hand:
                return self.weapons_data[self.state.left_hand]

    def is_equipped(self, weapon_id: str = None) -> bool:
        """Method to determine if weapon is equipped.
        Returns bool"""
        right_weapon = self.get_equipped("right_hand")
        left_weapon = self.get_equipped("left_hand")

        if not weapon_id:
            if right_weapon or left_weapon:
                return True
            else:
                return False
        if right_weapon and weapon_id == right_weapon["id"]:
            return True
        if left_weapon and weapon_id == left_weapon["id"]:
            return True
        return False

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
