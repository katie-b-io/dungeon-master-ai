from abc import ABC, abstractmethod
from dmai.utils.output_builder import OutputBuilder

from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Equipment(ABC):
    def __init__(self, equipment_data: dict, state: State, output_builder: OutputBuilder) -> None:
        """Equipment abstract class"""
        self.state = state
        self.output_builder = output_builder
        try:
            for key in equipment_data:
                self.__setattr__(key, equipment_data[key])

        except AttributeError as e:
            logger.error("(SESSION {s}) Cannot create equipment, incorrect attribute: {e}".format(e=e, s=self.state.session.session_id))
            raise

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> None:
        print("Using this doesn't do anything special")
        return True

    def stop(self) -> None:
        return True