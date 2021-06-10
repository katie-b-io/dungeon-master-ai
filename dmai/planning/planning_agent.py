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

    def _construct_problem_header(self, problem: str, domain: str) -> str:
        return "(define (problem {p}) (:domain {d})\n".format(p=problem, d=domain)
    
    def _construct_problem_footer(self) -> str:
        return ")\n"

    def _construct_objects(self, objects: list) -> str:
        """Method expects a list of tuples of one or two length.
        If length is two, the tuple is (object, type)"""
        objects_str = "(:objects\n"
        for obj in objects:
            if len(obj) == 1:
                objects_str += "{o}\n".format(o=obj[0])
            else:
                objects_str += "{o} - {t}\n".format(o=obj[0], t=obj[1])
        objects_str += ")\n"
        return objects_str
    
    def _construct_init(self, init: list) -> str:
        """Method expects a list of tuples of any length.
        Tuples will be constructed into PDDL strings, e.g. (one, two, three)
        becomes (one two three)"""
        init_str = "(:init\n"
        for obj in init:
            init_str += "({s})\n".format(s=" ".join(obj))
        init_str += ")\n"
        return init_str
    
    def _construct_goal(self, goal: list) -> str:
        """Method expects a list of tuples of any length.
        Tuples will be constructed into PDDL strings, e.g. (one, two, three)
        becomes (one two three)"""
        goal_str = "(:goal (and\n"
        for obj in goal:
            goal_str += "({g})\n".format(g=" ".join(obj))
        goal_str += "))\n"
        return goal_str
    