from dmai.utils.output_builder import OutputBuilder
from dmai.domain.equipment.equipment import Equipment
from dmai.game.state import State

from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Torch(Equipment):
    def __init__(self, equipment_data: dict, state: State, output_builder: OutputBuilder) -> None:
        Equipment.__init__(self, equipment_data, state, output_builder)

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> bool:
        logger.debug("Lighting a torch")
        if not self.state.torch_lit:
            self.state.light_torch()
            return True
        else:
            self.output_builder.append("You already have a lit torch.")
        return False

    def stop(self) -> bool:
        logger.debug("Extinguishing a torch")
        if self.state.torch_lit:
            self.state.extinguish_torch()
            return True
        return False