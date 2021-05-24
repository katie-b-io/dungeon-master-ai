from dmai.utils.loader import Loader
from dmai.utils.exceptions import UnrecognisedEquipment
from dmai.domain.equipment.torch import Torch
from dmai.domain.equipment.equipment import Equipment


class EquipmentCollection:

    # class variables
    equipment_data = dict()

    def __init__(self, equipment: str, proficiencies=None) -> None:
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
            equipment_map = {
                "torch": Torch
            }
            if equipment in equipment_map:
                equipment_obj = equipment_map[equipment]
            else:
                equipment_obj = Equipment
        else:
            msg = "Cannot create equipment {e} - it does not exist!".format(
                e=equipment
            )
            raise UnrecognisedEquipment(msg)
        return equipment_obj(self.equipment_data[equipment])

    def _load_equipment_data(self) -> None:
        """Set the self.equipment_data class variable data"""
        self.equipment_data = Loader.load_json("data/domain/equipment.json")
    
    def has_equipment(self, equipment_id: str) -> bool:
        """Method to return whether specified equipment exists"""
        return equipment_id in self.equipment
    
    def use_equipment(self, equipment_id: str) -> None:
        if self.has_equipment(equipment_id):
            self.equipment[equipment_id].use()
            
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
            
