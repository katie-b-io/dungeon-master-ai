from abc import ABC, abstractmethod

from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__, Config.session.session_id)


class Action(ABC):
    def __init__(self, **kwargs) -> None:
        """Action abstract class"""
        pass

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    @abstractmethod
    def execute(self, **kwargs) -> bool:
        pass
