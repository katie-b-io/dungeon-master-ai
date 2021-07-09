from dmai.domain.characters.character import Character
from dmai.game.state import State


class Rogue(Character):
    def __init__(self, character_data: dict, state: State) -> None:
        Character.__init__(self, character_data, state)
