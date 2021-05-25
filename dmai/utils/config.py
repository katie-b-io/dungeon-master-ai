import os


class Directories(object):
    @property
    def root(self) -> str:
        return os.path.abspath("")

    @property
    def data(self) -> str:
        return os.path.join(self.root, "data")

    @property
    def domain(self) -> str:
        return os.path.join(self.data, "domain")
    
    @property
    def adventure(self) -> str:
        return os.path.join(self.root, "adventures")


class ConfigMeta(type):
    _instances = {}

    def __new__(cls, name, bases, dict):
        instance = super().__new__(cls, name, bases, dict)
        instance.directory = Directories()
        return instance
    
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


