from abc import ABC, abstractmethod

from dmai.planning.planning_agent import PlanningAgent
from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class PlanningMonster(PlanningAgent):
    def __init__(self, **kwargs) -> None:
        """PlanningMonster class"""
        PlanningAgent.__init__(self, Config.planner.monster, "monster", **kwargs)
        
    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)
    
    def build_domain(self) -> None:
        pass

    def build_problem(self) -> None:
        pass
