from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class NPC():
    def __init__(self, state: State, npc_data: dict) -> None:
        """Main class for a npc"""
        self.state = state
        try:
            for key in npc_data:
                self.__setattr__(key, npc_data[key])

        except AttributeError as e:
            logger.error("(SESSION {s}) Cannot create NPC, incorrect attribute: {e}".format(s=self.state.session.session_id, e=e))
            raise

    def __repr__(self) -> str:
        return "NPC: {a}".format(a=self.name)
