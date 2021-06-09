from abc import ABC, abstractmethod

from dmai.planning.planner_adapter import PlannerAdapter
from dmai.planning.fast_downward_adapter import FastDownwardAdapter

from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class PlanningAgent(ABC):
    def __init__(self, planner: str, domain: str, problem: str) -> None:
        """PlanningAgent abstract class"""
        self.domain = domain
        self.problem = problem
        self.planner = self.get_planner(planner)
        
    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)
    
    @abstractmethod
    def build_domain(self) -> None:
        pass

    @abstractmethod
    def build_problem(self) -> None:
        pass

    def get_planner(self, planner: str) -> PlannerAdapter:
        """Returns an instance of a PlannerAdapter"""
        try:
            return self._planner_factory(planner)
        except ValueError as e:
            logger.error(e)
    
    def _planner_factory(self, planner: str) -> PlannerAdapter:
        """Construct an instance of a PlannerAdapter"""
        try:
            planner_map = {
                "fd": FastDownwardAdapter
            }
            planner = planner_map[planner]
            return planner(self.domain, self.problem)
        except (ValueError, KeyError) as e:
            msg = "Cannot create planner {p} - it does not exist!".format(p=planner)
            raise ValueError(msg)

    def prepare_next_move(self) -> None:
        """Method to prepare the next move.
        Planning agents build a plan"""
        self.build_domain()
        self.build_problem()
        self.planner.build_plan()

    def get_next_move(self) -> str:
        plan = self.planner.parse_plan()
        return plan[0]