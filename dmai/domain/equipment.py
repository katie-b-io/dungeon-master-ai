from dmai.utils.loader import Loader


class Equipment:

    # class variables
    equipment_data = dict()

    def __init__(self, equipment: str, proficiencies=None) -> None:
        """Equipment class"""
        self.equipment = equipment
        self.proficiencies = proficiencies
        self._load_equipment_data()

    def __repr__(self) -> str:
        return "Equipment:\n{a}".format(a=self.equipment)

    @classmethod
    def _load_equipment_data(cls) -> None:
        """Set the cls.equipment_data class variable data"""
        cls.equipment_data = Loader.load_json("data/domain/equipment.json")
    
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
            
