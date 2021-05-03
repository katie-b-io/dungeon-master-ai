from dmai.utils import Loader

class Features():
    
    # class variables
    feature_data = dict()
    
    def __init__(self, features: dict) -> None:
        '''Features class'''
        self.features = features
        self._load_feature_data()
        
    def __str__(self) -> str:
        return "Features:\n{a}".format(a=self.features)
    
    @classmethod
    def _load_feature_data(self) -> None:
        '''Set the self.feature_data class variable data'''
        self.feature_data = Loader.load_json("data/features.json")
        