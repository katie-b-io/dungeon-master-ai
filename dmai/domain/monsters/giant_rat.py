from dmai.domain.monsters.monster import Monster
from dmai.game.state import State

class GiantRat(Monster):
    def __init__(
        self,
        monster_data: dict,
        state: State,
        npc_data: dict = None,
        unique_id: str = None,
        unique_name: str = None,
    ) -> None:
        Monster.__init__(self, monster_data, state, npc_data, unique_id, unique_name)