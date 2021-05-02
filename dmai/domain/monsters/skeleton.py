from dmai.domain.monsters import Monster

class Skeleton(Monster):
    
    def __init__(self, monster_data: dict) -> None:
        Monster.__init__(self, monster_data)
