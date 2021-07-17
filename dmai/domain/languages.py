from dmai.utils.loader import Loader
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


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
        cls.language_data = Loader.load_domain("languages")

    def get_all(self) -> list:
        """Method to return all the languages"""
        all_languages = []
        for language_type in self.languages:
            for language in self.languages[language_type]:
                all_languages.append(self.language_data[language])
        return all_languages
