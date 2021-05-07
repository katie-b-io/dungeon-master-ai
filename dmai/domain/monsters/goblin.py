from dmai.domain.monsters.monster import Monster


class Goblin(Monster):
    def __init__(self, monster_data: dict) -> None:
        Monster.__init__(self, monster_data)
