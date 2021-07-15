from dmai.utils.output_builder import OutputBuilder
from dmai.domain.items.item import Item
from dmai.game.state import State
from dmai.utils.dice_roller import DiceRoller
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class PotionOfHealing(Item):
    def __init__(self, item_data: dict, state: State, output_builder: OutputBuilder) -> None:
        Item.__init__(self, item_data, state, output_builder)

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> bool:
        logger.debug("(SESSION {s}) Drinking a potion of healing".format(s=self.state.session.session_id))
        dice_spec = self.effects["hit_point"]["delta"]
        (roll_str, hp) = DiceRoller.roll_dice(dice_spec)
        self.output_builder.append(roll_str)
        self.state.heal(hp)
        return True
    