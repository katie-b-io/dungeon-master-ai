from dmai.domain.characters.character import Character


class Player:
    def __init__(self, character: Character) -> None:
        """Main class for the player"""
        self.name = None
        self.character = character

    def set_name(self, name: str) -> None:
        self.name = name

    @property
    def character_class(self) -> str:
        return self.character.name
