from dmai.nlg.nlg import NLG

class Room:
    def __init__(self, room_data: dict) -> None:
        """Main class for a room"""
        try:
            for key in room_data:
                self.__setattr__(key, room_data[key])
            
        except AttributeError as e:
            print("Cannot create room, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "Room: {a}".format(a=self.name)

    def enter(self) -> str:
        """Method for entering a room"""
        if not self.visited:
            self.visited = True
            return self.text["enter"]
        else:
            return NLG.enter_room(self.name)

    def cannot_enter(self, reason: str = None) -> str:
        """Method for not entering a room"""
        return NLG.cannot_move(self.name, reason)
