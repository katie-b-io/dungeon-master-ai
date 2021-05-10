from dmai.domain.monsters.monster import Monster


class Skeleton(Monster):
    def __init__(self, monster_data: dict, npc_data: dict = None) -> None:
        Monster.__init__(self, monster_data, npc_data)
