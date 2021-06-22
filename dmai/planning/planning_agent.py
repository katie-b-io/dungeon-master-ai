from abc import ABC, abstractmethod

from dmai.game.state import State
from dmai.planning.planner_adapter import PlannerAdapter
from dmai.planning.fast_downward_adapter import FastDownwardAdapter
from dmai.planning.planning_actions import planning_actions

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
            planner_map = {"fd": FastDownwardAdapter}
            planner = planner_map[planner]
            return planner(self.domain, self.problem)
        except (ValueError, KeyError) as e:
            msg = "Cannot create planner {p} - it does not exist!".format(
                p=planner)
            raise ValueError(msg)

    def prepare_next_move(self) -> bool:
        """Method to prepare the next move, e.g. planning agents build a plan.
        Returns bool for whether plan was built."""
        self.build_domain()
        self.build_problem()
        # TODO do something with succeed
        succeed = self.planner.build_plan()
        if succeed:
            self.planner.parse_plan()
        return succeed

    def get_next_move(self) -> str:
        if bool(self.planner.plan):
            return self.planner.to_natural_language(self.planner.plan[0])
        else:
            return False
    
    def perform_next_move(self) -> None:
        move = self.planner.pop_move()
        if move:
            self.planner.call_function(move)

    ################################################
    # Methods for PDDL problem files
    def _construct_problem_header(self, problem: str, domain: str) -> str:
        return "(define (problem {p}) (:domain {d})\n".format(p=problem,
                                                              d=domain)

    def _construct_problem_footer(self) -> str:
        return ")\n"

    def _construct_objects(self, objects: list) -> str:
        """Method expects a list of tuples of two length.
        If length is two, the tuple is (object, type)"""
        objects_str = "(:objects\n"
        for obj in objects:
            objects_str += "{o} - {t}\n".format(o=obj[0], t=obj[1])
        objects_str += ")\n"
        return objects_str

    def _construct_init(self, init: list) -> str:
        """Method expects a list of list of any length.
        Tuples will be constructed into PDDL strings, e.g. (one, two, three)
        becomes (one two three)"""
        init_str = "(:init\n"
        for obj in init:
            init_str += "({s})\n".format(s=" ".join(obj))
        init_str += ")\n"
        return init_str

    def _construct_goal(self, goal: list, alt_goal: list = None) -> str:
        """Method expects a list of list of any length.
        Tuples will be constructed into PDDL strings, e.g. (one, two, three)
        becomes (one two three)"""
        if alt_goal:
            goal_str = "(:goal (or (and\n"
        else:
            goal_str = "(:goal (and\n"
        for obj in goal:
            if len(obj) == 1:
                goal_str += "({s})\n".format(s=obj[0])
            else:
                if obj[0] == "not":
                        goal_str += "(not "
                        goal_str += "({g})".format(g=" ".join(obj[1:]))
                        goal_str += ")\n"
                else:
                    goal_str += "({g})\n".format(g=" ".join(obj))
        if alt_goal:
            goal_str += ")\n(and\n"
            for obj in alt_goal:
                if len(obj) == 1:
                    goal_str += "({s})\n".format(s=obj[0])
                else:
                    if obj[0] == "not":
                        goal_str += "(not "
                        goal_str += "({g})".format(g=" ".join(obj[1:]))
                        goal_str += ")\n"
                    else:
                        goal_str += "({g})\n".format(g=" ".join(obj))
        if alt_goal:
            goal_str += ")))\n"
        else:
            goal_str += "))\n"
        return goal_str

    ################################################
    # Methods for PDDL domain files
    def _construct_domain_header(self, domain: str) -> str:
        return "(define (domain {d})\n".format(d=domain)

    def _construct_domain_footer(self) -> str:
        return ")\n"

    def _construct_requirements(self) -> str:
        requirements_str = "(:requirements \n"
        requirements_str += ":strips\n"
        requirements_str += ":typing\n"
        requirements_str += ":conditional-effects\n"
        requirements_str += ":negative-preconditions\n"
        requirements_str += ":equality\n"
        requirements_str += ":disjunctive-preconditions\n"
        requirements_str += ")\n"
        return requirements_str

    def _construct_types(self, types: list) -> str:
        """Method expects a list of dicts of any length.
        Dicts will be constructed into PDDL strings, e.g.
        {
            "type": "attitude",
            "subtypes": ["indifferent", "friendly", "hostile"]
        }
        becomes (indifferent friendly hostile - attitude)"""
        types_str = "(:types\n"
        for obj in types:
            t = obj["type"]
            subtypes = " ".join(obj["subtypes"])
            types_str += "{s} - {t}\n".format(s=subtypes, t=t)
        types_str += ")\n"
        return types_str

    def _construct_predicates(self, predicates: list) -> str:
        """Method expects a list of dicts of any length.
        Dicts will be constructed into PDDL strings, e.g.
        {
            "predicate": "can_attack_roll",
            "params": [
                (parameter, type)
                ("player", "player"),
                ("target", "object")
            ]
        }
        becomes (can_attack_roll ?player - player ?target - object)"""
        predicates_str = "(:predicates\n"
        for predicate in predicates:
            p = predicate["predicate"]
            if predicate["params"]:
                params = ""
                for param in predicate["params"]:
                    params += " ?{p} - {t}".format(p=param[0], t=param[1])
                predicates_str += "({p}{params})\n".format(p=p, params=params)
            else:
                predicates_str += "({p})\n".format(p=p)
        predicates_str += ")\n"
        return predicates_str

    def _construct_actions(self, actions: list) -> str:
        """Method expects a list of action IDs. 
        Action PDDL strings will be looked up and appended to string"""
        actions_str = ""
        for action in actions:
            actions_str += "{a}\n".format(a=planning_actions[action]["pddl"])
        return actions_str