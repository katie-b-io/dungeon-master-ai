from dmai.utils.loader import Loader
from dmai.domain.characters.character import Character
from dmai.domain.characters.fighter import Fighter
from dmai.domain.characters.wizard import Wizard
from dmai.domain.characters.rogue import Rogue
from dmai.domain.characters.cleric import Cleric


class CharacterCollection:

    # class variables
    character_data = dict()

    def __init__(self) -> None:
        """CharacterCollection class"""
        self._load_character_data()
        self.characters = dict()

    def __repr__(self) -> str:
        character_list = self.characters.keys()
        character_str = "{c} is storing the following characters: {cl}".format(
            c=self.__class__.__name__, cl=", ".join(character_list)
        )
        return character_str

    @classmethod
    def _load_character_data(self) -> None:
        """Set the self.character_data class variable data"""
        self.character_data = Loader.load_json("data/characters.json")

    def get_all(self) -> dict:
        return self.character_data

    def get_all_names(self) -> list:
        return [self.character_data[c]["name"] for c in self.character_data]

    def get_character(self, character: str) -> Character:
        """Return a character of specified type"""
        character_obj = None
        try:
            character_obj = self._character_factory(character)
            self.characters[character_obj.name] = character_obj
        except ValueError as e:
            print(e)
        return character_obj

    def _character_factory(self, character: str) -> Character:
        """Construct a character of specified type"""
        character = character.lower()
        if character in self.character_data.keys():
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
        return character_obj(self.character_data[character])
