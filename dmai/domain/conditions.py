from dmai.utils.loader import Loader


class Conditions:

    # class variables
    condition_data = dict()

    def __init__(self) -> None:
        """Conditions class"""
        self.conditions = dict()
        self._load_condition_data()

    def __repr__(self) -> str:
        return "Conditions:\n{a}".format(a=self.conditions)

    @classmethod
    def _load_condition_data(cls) -> None:
        """Set the cls.condition_data class variable data"""
        cls.condition_data = Loader.load_domain("conditions")
