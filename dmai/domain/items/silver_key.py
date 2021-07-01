from dmai.utils.output_builder import OutputBuilder
from dmai.domain.items.item import Item
from dmai.game.state import State
from dmai.utils.dice_roller import DiceRoller

from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class SilverKey(Item):
    def __init__(self, item_data: dict) -> None:
        Item.__init__(self, item_data)

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> bool:
        logger.debug("Using silver key")
        puzzle = State.get_current_room().puzzles.get_puzzle("unlock")
        if puzzle:
            if puzzle["item"] == self.id:
                OutputBuilder.append("Door unlocked woo!")
                room1 = puzzle.id.split("---")[0]
                room2 = puzzle.id.split("---")[1]
                State.unlock_door(room1, room2)
        return True
    