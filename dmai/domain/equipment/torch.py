from dmai.domain.equipment.equipment import Equipment
from dmai.game.state import State

from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Torch(Equipment):
    def __init__(self, equipment_data: dict) -> None:
        Equipment.__init__(self, equipment_data)

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> None:
        logger.debug("Lighting a torch")
        if not State.torch_lit:
            State.light_torch()

    def stop(self) -> None:
        logger.debug("Extinguishing a torch")
        if State.torch_lit:
            State.extinguish_torch()