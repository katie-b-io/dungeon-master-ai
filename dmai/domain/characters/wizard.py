from dmai.domain.characters.character import Character


class Wizard(Character):
    def __init__(self, character_data: dict) -> None:
        Character.__init__(self, character_data)
