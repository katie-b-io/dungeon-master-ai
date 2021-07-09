from dmai.domain.items.item import Item
from dmai.game.state import State
from dmai.utils.dice_roller import DiceRoller
from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class PotionOfHealing(Item):
    def __init__(self, item_data: dict, state: State) -> None:
        Item.__init__(self, item_data)
        self.state = state

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> bool:
        logger.debug("Drinking a potion of healing")
        dice_spec = self.effects["hit_point"]["delta"]
        hp = DiceRoller.roll_dice(dice_spec)
        self.state.heal(hp, self.state.get_player().hp_max)
        return True
    