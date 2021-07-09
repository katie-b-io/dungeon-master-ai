from abc import ABC, abstractmethod

from dmai.game.state import State
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Agent(ABC):
    def __init__(self, state: State, **kwargs) -> None:
        """Agent abstract class"""
        self.state = state
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
        logger.debug("Printing next move")
        move = self.agent.get_next_move()
        OutputBuilder.append(move)
        return bool(move)

    def perform_next_move(self) -> bool:
        """Method to perform the next move"""
        logger.debug("Performing the next move")
        self.agent.perform_next_move()
        
        # TODO parse the PDDL and act accordinging 
        # e.g. Steps of combat:
        # 1. declare target
        # 1. attack roll - damage_roll() if exceeds target AC else return
        # 2. damage roll - apply_damage()"""