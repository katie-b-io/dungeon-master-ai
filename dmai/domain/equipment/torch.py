from dmai.domain.equipment.equipment import Equipment


class Torch(Equipment):
    def __init__(self, equipment_data: dict) -> None:
        Equipment.__init__(self, equipment_data)
    
    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)
    
    def use(self) -> None:
        print("Using the torch!")