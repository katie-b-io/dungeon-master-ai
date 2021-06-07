from dmai.planning.planner_adapter import PlannerAdapter
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class FastDownwardAdapter(PlannerAdapter):
    def __init__(self) -> None:
        """FastDownwardAdapter abstract class"""
        pass
        
    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)
    
    def build_domain(self) -> None:
        pass

    def build_problem(self) -> None:
        pass
    
    def build_plan(self) -> None:
        pass

    def parse_plan(self) -> None:
        pass