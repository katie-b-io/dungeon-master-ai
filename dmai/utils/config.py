import os


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

    class Directories(object):
        root = os.path.abspath("")

        @classmethod
        def set_root(cls, root) -> None:
            cls.root = root
            print(root)

        @property
        def data(self) -> str:
            return os.path.join(self.root, "data")

        @property
        def domain(self) -> str:
            return os.path.join(self.data, "domain")

        @property
        def adventure(self) -> str:
            return os.path.join(self.root, "adventures")

    # class variables
    directory = Directories()

    @classmethod
    def set_root(cls, root: str) -> None:
        """Method to set the dmai root directory"""
        cls.directory.set_root(root)
