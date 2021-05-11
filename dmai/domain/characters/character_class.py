from dmai.utils.loader import Loader


class CharacterClass:

    # class variables
    char_class_data = dict()

    def __init__(self, char_class: dict) -> None:
        """CharacterClass class"""
        self._load_char_class_data()

        try:
            self.char_class = list(char_class.keys())[0]
            self.level = char_class[self.char_class]["level"]
            if char_class[self.char_class]["subclass"]:
                self.subclass = char_class[self.char_class]["subclass"]
            else:
                self.subclass = None

            for key in self.char_class_data[self.char_class]:
                self.__setattr__(key, self.char_class_data[self.char_class][key])

        except KeyError as e:
            print("Class does not exist: {c}".format(c=e))
            raise
        except AttributeError as e:
            print("Cannot create class, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "Class: {a}".format(a=self.name)

    @classmethod
    def _load_char_class_data(cls) -> None:
        """Set the cls.char_class_data class variable data"""
        cls.char_class_data = Loader.load_json("data/domain/classes.json")
