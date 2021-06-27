from dmai.utils.loader import Loader
from dmai.utils.exceptions import UnrecognisedEquipment
from dmai.domain.equipment.torch import Torch
from dmai.domain.equipment.equipment import Equipment


class EquipmentCollection:

    # class variables
    equipment_data = dict()

    def __init__(self, equipment: dict, proficiencies=None) -> None:
        """EquipmentCollection class"""
        self.equipment = equipment
        self.proficiencies = proficiencies
        self._load_equipment_data()

        # prepare the equipment
        for equipment_id in self.equipment:
            equipment_obj = self._equipment_factory(equipment_id)
            self.equipment[equipment_id] = {
                "equipment": equipment_obj,
                "quantity": self.equipment[equipment_id]
            }

    def __repr__(self) -> str:
        return "Equipment collection:\n{a}".format(a=self.equipment)

    def _equipment_factory(self, equipment: str) -> Equipment:
        """Construct an equipment of specified type"""
        if equipment in self.equipment_data.keys():
            equipment_map = {"torch": Torch}
            if equipment in equipment_map:
                equipment_obj = equipment_map[equipment]
            else:
                equipment_obj = Equipment
        else:
            msg = "Cannot create equipment {e} - it does not exist!".format(
                e=equipment)
            raise UnrecognisedEquipment(msg)
        return equipment_obj(self.equipment_data[equipment])

    def _load_equipment_data(self) -> None:
        """Set the self.equipment_data class variable data"""
        self.equipment_data = Loader.load_domain("equipment")

    def _check_equipment(self, equipment_id: str) -> bool:
        """Method to return whether specified equipment exists.
        Returns a boolean."""
        if equipment_id not in self.equipment_data:
            msg = "Equipment {e} does not exist!".format(e=equipment_id)
            raise UnrecognisedEquipment(msg)
        return True

    def has_equipment(self, equipment_id: str) -> tuple:
        """Method to return whether specified equipment exists.
        Returns a tuple with the boolean and a string with a reason."""
        try:
            if self._check_equipment(equipment_id):
                if not equipment_id in self.equipment:
                    return (False, "not equipped")
                if not self.quantity_above_zero(equipment_id):
                    return (False, "quantity")
                return (True, "")
            return (False, "unknown")
        except UnrecognisedEquipment:
            return (False, "unknown")

    def quantity_above_zero(self, equipment_id: str) -> bool:
        """Method to return whether quantity of specified equipment is above zero"""
        if equipment_id in self.equipment:
            return self.equipment[equipment_id]["quantity"] > 0

    def use_equipment(self, equipment_id: str) -> bool:
        """Method to use specified equipment.
        Returns bool for whether equipment was used"""
        try:
            if self._check_equipment(equipment_id):
                (has_equipment, reason) = self.has_equipment(equipment_id)
                if has_equipment:
                    self.equipment[equipment_id][
                        "quantity"] = self.equipment[equipment_id]["quantity"] - 1
                    return self.equipment[equipment_id]["equipment"].use()
            return False
        except UnrecognisedEquipment:
            return False

    def stop_using_equipment(self, equipment_id: str) -> bool:
        """Method to stop using specified equipment.
        Returns bool for whether equipment was stopped being used"""
        try:
            if self._check_equipment(equipment_id):
                if equipment_id in self.equipment:
                    return self.equipment[equipment_id]["equipment"].stop()
            return False
        except UnrecognisedEquipment:
            return False

    def get_all(self) -> list:
        """Return a list with all the equipment ids"""
        return self.equipment.keys()

    def get_formatted(self, equipment_id) -> str:
        """Return the formatted equipment with quantities"""
        if equipment_id in self.equipment_data:
            quantity = self.equipment[equipment_id]
            equipment = self.equipment_data[equipment_id]
            if equipment_id == "rope_hempen":
                return "{q} ft {e}".format(q=quantity, e=equipment["name"])
            if self.equipment[equipment_id] == 1:
                return equipment["name"]
            else:
                return "{q} {e}".format(q=quantity, e=equipment["name"])

    def get_proficient(self) -> str:
        """Return the proficient equipment in a list"""
        all_profs = []
        for prof_type in self.proficiencies:
            for prof in self.proficiencies[prof_type]:
                all_profs.append(self.equipment_data[prof])
        return all_profs
