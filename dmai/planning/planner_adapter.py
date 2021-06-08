from abc import ABC, abstractmethod

from dmai.utils.logger import get_logger

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