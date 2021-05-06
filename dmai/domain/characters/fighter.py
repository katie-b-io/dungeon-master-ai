from dmai.domain.characters import Character


class Fighter(Character):
    def __init__(self, character_data: dict) -> None:
        Character.__init__(self, character_data)
