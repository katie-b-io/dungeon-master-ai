from abc import ABC, abstractmethod

from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Agent(ABC):
    def __init__(self, **kwargs) -> None:
        """Agent abstract class"""
        self.agent = self.get_agent(**kwargs)

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    @abstractmethod
    def get_agent(self, **kwargs):
        pass

    def prepare_next_move(self) -> bool:
        logger.debug("Preparing next move")
        return self.agent.prepare_next_move()

    def print_next_move(self) -> bool:
        """Method to print the next move"""
        logger.debug("Getting next move")
        move = self.agent.get_next_move()
        OutputBuilder.append(move)
        return bool(move)