from abc import ABC, abstractmethod

from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger
from dmai.planning.planning_actions import planning_actions
from dmai.game.state import State

logger = get_logger(__name__)


class PlannerAdapter(ABC):
    def __init__(self, domain: str, problem: str) -> None:
        """PlannerAdapter abstract class"""
        self.domain = domain
        self.problem = problem

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    @abstractmethod
    def build_plan(self) -> None:
        pass

    @abstractmethod
    def parse_plan(self) -> None:
        pass
    
    def to_natural_language(self, step: str) -> str:
        """Method to convert a step in a plan to natural language"""
        return step
    
    def call_function(self, step: str) -> object:
        """Method to convert a step to an function"""
        step = step.replace("(", "").replace(")", "")
        action = step.split(" ")[0]
        params = step.split(" ")[1:]
        if action in planning_actions:
            function = planning_actions[action]["function"]
            # if the function is NLG, it needs to be wrapped in the OutputBuilder
            if function.__self__.__name__ == "NLG":
                params[0] = State.get_name(params[0])
                OutputBuilder.append(function(*params))
        