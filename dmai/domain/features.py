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
    def _load_feature_data(cls) -> None:
        """Set the cls.feature_data class variable data"""
        cls.feature_data = Loader.load_json("data/domain/features.json")
        cls.feature_data.update(Loader.load_json("data/domain/monster_features.json"))

    def get_all(self) -> list:
        """Method to return all the features"""
        return [self.feature_data[feature] for feature in self.features]
    
    def get_description(self, feature_id) -> str:
        """Method to return the feature description"""
        if feature_id in self.feature_data:
            return self.feature_data[feature_id]["description"]
    
    def contains(self, feature_id) -> bool:
        """Method to return bool for whether feature is in features"""
        return feature_id in self.features