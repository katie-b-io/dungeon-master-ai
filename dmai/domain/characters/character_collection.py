from dmai.utils.loader import Loader
from dmai.domain.characters.character import Character
from dmai.domain.characters.fighter import Fighter
from dmai.domain.characters.wizard import Wizard
from dmai.domain.characters.rogue import Rogue
from dmai.domain.characters.cleric import Cleric


class CharacterCollectionMeta(type):
    _instances = {}

    def __new__(cls, name, bases, dict):
        instance = super().__new__(cls, name, bases, dict)
        instance.character_data = Loader.load_json("data/characters.json")
        return instance

    def __call__(cls, *args, **kwargs) -> None:
        """CharacterCollection static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    
class CharacterCollection(metaclass=CharacterCollectionMeta):

    # class variables
    character_data = dict()

    def __init__(self) -> None:
        """CharacterCollection class"""
        pass

    @classmethod
    def __repr__(cls) -> str:
        character_list = cls.character_data.keys()
        character_str = "{c} is storing the following characters: {cl}".format(
            c=cls.__class__.__name__, cl=", ".join(character_list)
        )
        return character_str

    @classmethod
    def get_all_names(cls) -> list:
        return [cls.character_data[c]["name"] for c in cls.character_data]

    @classmethod
    def get_character(cls, character: str) -> Character:
        """Return a character of specified type"""
        character_obj = None
        try:
            character_obj = cls._character_factory(character)
        except ValueError as e:
            print(e)
        return character_obj

    @classmethod
    def _character_factory(cls, character: str) -> Character:
        """Construct a character of specified type"""
        character = character.lower()
        if character in cls.character_data.keys():
            character_map = {
                "cleric": Cleric,
                "fighter": Fighter,
                "rogue": Rogue,
                "wizard": Wizard,
            }
            character_obj = character_map[character]
        else:
            msg = "Cannot create character class {c} - it does not exist!".format(
                c=character
            )
            raise ValueError(msg)
        return character_obj(cls.character_data[character])
