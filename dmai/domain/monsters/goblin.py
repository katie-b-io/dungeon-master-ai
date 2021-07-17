from dmai.utils.output_builder import OutputBuilder
from dmai.domain.monsters.monster import Monster
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)

class Goblin(Monster):
    def __init__(
        self,
        monster_data: dict,
        state: State,
        output_builder: OutputBuilder,
        npc_data: dict = None,
        unique_id: str = None,
        unique_name: str = None,
    ) -> None:
        Monster.__init__(self, monster_data, state, output_builder, npc_data, unique_id, unique_name)
