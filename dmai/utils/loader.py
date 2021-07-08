import json
import os

from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class LoaderMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> None:
        """Loader static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Loader(metaclass=LoaderMeta):
    def __init__(self) -> None:
        """Loader static class"""
        pass

    @staticmethod
    def load_adventure(adventure: str) -> dict:
        """Loads specified adventure data"""
        adventure = "{a}.json".format(a=adventure)
        file = os.path.join(Config.directory.adventure, adventure)
        return Loader.load_json(file)

    @staticmethod
    def load_domain(domain: str) -> dict:
        """Loads specified domain data"""
        domain = "{d}.json".format(d=domain)
        file = os.path.join(Config.directory.domain, domain)
        return Loader.load_json(file)

    @staticmethod
    def load_json(file: str) -> dict:
        """Loads a data structure from JSON file"""
        json_data = dict()
        try:
            with open(file, mode="r") as f:
                json_data = json.load(f)
        except FileNotFoundError:
            logger.error("{f} does not exist!".format(f=file))

        return json_data
