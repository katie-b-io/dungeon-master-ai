class MoneyMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> None:
        """Money static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Money(metaclass=MoneyMeta):
    def __init__(self) -> None:
        """Money static class"""
        pass

    @staticmethod
    def get_formatted(cp: int) -> str:
        """Converted an integer value of copper pieces into a formatted string"""
        pp = int(cp / 1000)
        cp = cp % 1000
        gp = int(cp / 100)
        cp = cp % 100
        sp = int(cp / 10)
        cp = cp % 10
        return "PP: {p}\nGP: {g}\nSP: {s}\nCP: {c}".format(p=pp,
                                                           g=gp,
                                                           s=sp,
                                                           c=cp)
