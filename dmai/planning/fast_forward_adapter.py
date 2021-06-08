from dmai.planning.planner_adapter import PlannerAdapter
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class FastForwardAdapter(PlannerAdapter):
    def __init__(self) -> None:
        """FastForwardAdapter class"""
        pass
        
    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)
    
    def build_plan(self) -> None:
        pass

    def parse_plan(self) -> None:
        pass