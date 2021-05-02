from dmai.domain.monsters import MonsterCollection
from dmai.domain.characters import CharacterCollection, Character

class Domain():
    
    def __init__(self) -> None:
        '''Domain holds all the information about the world'''
        self.monsters = None
        
    def load_all(self) -> None:
        '''Function to load all the elements of the domain into the
        Domain object'''
        self.monsters = MonsterCollection()
        self.characters = CharacterCollection()
        
    @property
    def char_class_select(self) -> str:
        '''Return the possible character classes for selection'''
        select_str = "Select a character class from the following choices:\n{c}\n" \
        .format(c="\n".join(self.characters.get_all_names()))
        return select_str
    
    def get_character(self, character: str) -> Character:
        return self.characters.get_character(character)