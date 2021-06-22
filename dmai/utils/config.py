import os
import uuid
from pathlib import Path


class ConfigMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> None:
        """Config static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=ConfigMeta):
    def __init__(self) -> None:
        """Config static class"""
        pass

    ################################################################
    class Directories(object):
        root = os.path.abspath("")

        @classmethod
        def set_root(cls, root) -> None:
            cls.root = root

        @property
        def data(self) -> str:
            return os.path.join(self.root, "data")

        @property
        def domain(self) -> str:
            return os.path.join(self.data, "domain")

        @property
        def adventure(self) -> str:
            return os.path.join(self.root, "adventures")

        @property
        def output(self) -> str:
            path = os.path.join(self.root, "output")
            if not os.path.exists(path):
                Path(path).mkdir(parents=True, exist_ok=True)
            return path

        @property
        def planning(self) -> str:
            path = os.path.join(self.output, "planning")
            if not os.path.exists(path):
                Path(path).mkdir(parents=True, exist_ok=True)
            return path

        @property
        def test(self) -> str:
            return os.path.join(self.root, "tests")

        @property
        def planning_test(self) -> str:
            return os.path.join(self.test, "planning")

    ################################################################
    class Agents(object):
        player = "planning"
        monster = "planning"

        @classmethod
        def set_player(cls, agent: str) -> None:
            cls.player = agent

        @classmethod
        def set_monster(cls, agent: str) -> None:
            cls.monster = agent

    ################################################################
    class Planners(object):
        player = "fd"
        monster = "fd"

        @classmethod
        def set_player(cls, agent: str) -> None:
            cls.player = agent

        @classmethod
        def set_monster(cls, agent: str) -> None:
            cls.monster = agent

    ################################################################
    # class variables
    cleanup = False
    directory = Directories()
    agent = Agents()
    planner = Planners()

    @classmethod
    def set_root(cls, root: str) -> None:
        """Method to set the dmai root directory"""
        cls.directory.set_root(root)

    @classmethod
    def set_uuid(cls) -> None:
        """Method to set the UUID"""
        cls.uuid = str(uuid.uuid1())

    @classmethod
    def cleanup_on_exit(cls) -> None:
        """Method to set cleanup status"""
        cls.cleanup = True