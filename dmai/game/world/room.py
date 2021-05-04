
class Room():
    
    def __init__(self, room_data: dict) -> None:
        '''Main class for a room'''
        try:
            for key in room_data:
                self.__setattr__(key, room_data[key])
            
        except AttributeError as e:
            print("Cannot create room, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "Room: {a}".format(a=self.name)