from dmai.utils.output_builder import OutputBuilder
from dmai.domain.characters.character import Character
from dmai.game.state import State


class Rogue(Character):
    def __init__(self, character_data: dict, state: State, output_builder: OutputBuilder) -> None:
        Character.__init__(self, character_data, state, output_builder)
