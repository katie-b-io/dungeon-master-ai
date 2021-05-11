from dmai.utils.loader import Loader


class Languages:

    # class variables
    language_data = dict()

    def __init__(self, languages: dict) -> None:
        """Languages class"""
        self.languages = languages
        self._load_language_data()

    def __repr__(self) -> str:
        return "Languages:\n{a}".format(a=self.languages)

    @classmethod
    def _load_language_data(cls) -> None:
        """Set the cls.language_data class variable data"""
        cls.language_data = Loader.load_json("data/domain/languages.json")
