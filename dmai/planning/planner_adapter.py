from abc import ABC, abstractmethod

from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger
from dmai.planning.planning_actions import PlanningActions
from dmai.game.state import State, State

logger = get_logger(__name__)


class PlannerAdapter(ABC):
    def __init__(self, domain: str, problem: str, state: State, output_builder: OutputBuilder) -> None:
        """PlannerAdapter abstract class"""
        self.domain = domain
        self.problem = problem
        self.state = state
        self.output_builder = output_builder
        self.plan = None
        self.planning_actions = PlanningActions(state)

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
            if not self.plan:
                logger.debug("(SESSION {s}) Plan failed".format(s=self.state.session.session_id))
        if len(self.plan) > 0:
            return self.plan.pop(0)
        
    def to_natural_language(self, step: str) -> str:
        """Method to convert a step in a plan to natural language"""
        step = step.replace("(", "").replace(")", "").replace("\n", "")
        params = step.split(" ")
        action = params[0]
        for planning_action_id in self.planning_actions.actions:
            planning_action = self.planning_actions.actions[planning_action_id]
            if "action" in planning_action:
                if action == planning_action["action"]:
                    string_params = {}
                    for p, i in planning_action["string_param_indices"].items():
                        string_params[p] = self.state.get_name(params[i])
                    return planning_action["string"].format(**string_params)
        return step
    
    def call_function(self, step: str) -> object:
        """Method to convert a step to an function"""
        step = step.replace("(", "").replace(")", "").replace("\n", "")
        action = step.split(" ")[0]
        params = step.split(" ")[1:]
        
        if action in self.planning_actions.actions:
            func = self.planning_actions.actions[action]["func"]
            # if the function is NLG, it needs to be wrapped in the self.output_builder
            if hasattr(func, ".__self__") and func.__self__.__name__ == "NLG":
                self.output_builder.append(func(*params))
            else:
                func(*params)
        