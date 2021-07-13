from dmai.utils.output_builder import OutputBuilder
from dmai.domain.items.item import Item
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class SilverKey(Item):
    def __init__(self, item_data: dict, state: State, output_builder: OutputBuilder) -> None:
        Item.__init__(self, item_data, state, output_builder)

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> bool:
        logger.debug("Using silver key")
        for puzzle in self.state.get_current_room().puzzles.get_all_puzzles():
            if "unlock" in puzzle.solutions:
                if puzzle.solutions["unlock"]["item"] == self.id:
                    if not puzzle.id in self.state.solved_puzzles:
                        self.output_builder.append(puzzle.solutions["unlock"]["say"])
                        room1 = puzzle.id.split("---")[0]
                        room2 = puzzle.id.split("---")[1]
                        self.state.unlock_door(room1, room2)
                        return True
                    else:
                        self.output_builder.append("This key is no longer useful as the door is already open.")
                        return False
        self.output_builder.append("The purpose of this key is not clear yet.")
    