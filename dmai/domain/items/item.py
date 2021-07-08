from abc import ABC, abstractmethod

from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Item(ABC):
    def __init__(self, item_data: dict) -> None:
        """Item abstract class"""
        try:
            for key in item_data:
                self.__setattr__(key, item_data[key])

        except AttributeError as e:
            logger.error(
                "Cannot create item, incorrect attribute: {e}".format(
                    e=e))
            raise

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def use(self) -> None:
        print("Using this doesn't do anything special")
        return True

    def stop(self) -> None:
        return True