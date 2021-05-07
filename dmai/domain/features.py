from dmai.utils.loader import Loader


class Features:

    # class variables
    feature_data = dict()

    def __init__(self, char_class=None, race=None, features: list = None) -> None:
        """Features class"""
        self._load_feature_data()
        self.features = list()

        if features:
            self.features.extend(features)

        if char_class:
            self.features.extend(char_class.features)

        if race:
            self.features.extend(race.traits)

    def __repr__(self) -> str:
        return "Features:\n{a}".format(a=self.features)

    @classmethod
    def _load_feature_data(self) -> None:
        """Set the self.feature_data class variable data"""
        self.feature_data = Loader.load_json("data/features.json")
        self.feature_data.update(Loader.load_json("data/monster_features.json"))
