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
        self.plan = None

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    @abstractmethod
    def build_plan(self) -> None:
        pass

    @abstractmethod
    def parse_plan(self) -> None:
        pass
    
    def pop_move(self) -> str:
        """Method to pop the first action from the plan"""
        if not self.plan:
            self.parse_plan()
        if len(self.plan) > 0:
            return self.plan.pop(0)
        
    def to_natural_language(self, step: str) -> str:
        """Method to convert a step in a plan to natural language"""
        return step
    
    def call_function(self, step: str) -> object:
        """Method to convert a step to an function"""
        step = step.replace("(", "").replace(")", "").replace("\n", "")
        action = step.split(" ")[0]
        params = step.split(" ")[1:]
        
        if action in planning_actions:
            func = planning_actions[action]["func"]
            # if the function is NLG, it needs to be wrapped in the OutputBuilder
            if hasattr(func, ".__self__") and func.__self__.__name__ == "NLG":
                OutputBuilder.append(func(*params))
            else:
                func(*params)
        