from abc import ABC, abstractmethod
from dmai.utils.output_builder import OutputBuilder
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Item(ABC):
    def __init__(self, item_data: dict, state: State, output_builder: OutputBuilder) -> None:
        """Item abstract class"""
        self.state = state
        self.output_builder = output_builder
        try:
            for key in item_data:
                self.__setattr__(key, item_data[key])

        except AttributeError as e:
            logger.error("(SESSION {s}) Cannot create item, incorrect attribute: {e}".format(s=self.state.session.session_id, e=e))
            raise

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> None:
        self.output_builder.append("Using this doesn't do anything special")
        return True

    def stop(self) -> None:
        return True