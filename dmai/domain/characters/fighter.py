from dmai.domain.characters.character import Character
from dmai.game.state import State


class Fighter(Character):
    def __init__(self, character_data: dict, state: State) -> None:
        Character.__init__(self, character_data, state)
