from dmai.utils.loader import Loader
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class CharacterClass:

    # class variables
    char_class_data = dict()

    def __init__(self, char_class: dict) -> None:
        """CharacterClass class"""
        self._load_char_class_data()

        try:
            self.char_class = list(char_class.keys())[0]
            self.level = char_class[self.char_class]["level"]
            self.subclass = char_class[self.char_class]["subclass"]
            if self.subclass:
                self.subclass = self.char_subclass_data[self.subclass]

            for key in self.char_class_data[self.char_class]:
                self.__setattr__(key,
                                 self.char_class_data[self.char_class][key])

        except KeyError as e:
            logger.error("Class does not exist: {c}".format(c=e))
            raise
        except AttributeError as e:
            logger.error(
                "Cannot create class, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "Class: {a}".format(a=self.name)

    @classmethod
    def _load_char_class_data(cls) -> None:
        """Set the cls.char_class_data class variable data"""
        cls.char_class_data = Loader.load_domain("classes")
        cls.char_subclass_data = Loader.load_domain("subclasses")

    def get_formatted_class(self) -> str:
        """Return fully formatted character class"""
        if self.subclass:
            return "{n} ({s}) {l}".format(n=self.name,
                                          s=self.subclass["name"],
                                          l=self.level)
        else:
            return "{n} {l}".format(n=self.name, l=self.level)

    def get_proficiencies(self, prof_type) -> list:
        """Return a list of proficiencies of specified type"""
        if prof_type in self.proficiencies:
            return self.proficiencies[prof_type]
