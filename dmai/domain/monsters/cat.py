from dmai.domain.monsters.monster import Monster


class Cat(Monster):
    def __init__(self, monster_data: dict, npc_data: dict = None, unique_id: str = None) -> None:
        Monster.__init__(self, monster_data, npc_data, unique_id)
