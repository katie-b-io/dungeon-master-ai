from dmai.utils.output_builder import OutputBuilder
from dmai.domain.characters.character import Character
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Wizard(Character):
    def __init__(self, character_data: dict, state: State, output_builder: OutputBuilder) -> None:
        Character.__init__(self, character_data, state, output_builder)
