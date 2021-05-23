from dmai.utils.output_builder import OutputBuilder
from dmai.nlg.nlg import NLG
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Room:
    def __init__(self, room_data: dict) -> None:
        """Main class for a room"""
        try:
            for key in room_data:
                self.__setattr__(key, room_data[key])
            
        except AttributeError as e:
            logger.error("Cannot create room, incorrect attribute: {e}".format(e=e))
            raise
        
        text_map = {
            "enter": self.enter,
            "exit": print,
            "visibility": self.visibility
        }
        
        # populate the self.text object
        for text_type in self.text:
            text = self.text[text_type]
            self.text[text_type] = {
                "text": text,
                "read": False,
                "trigger": text_map[text_type]
            }

    def __repr__(self) -> str:
        return "Room: {a}".format(a=self.name)

    def enter(self) -> str:
        """Method when entering a room"""
        if not self.visited:
            self.text["enter"]["read"] = True
            self.visited = True
            return self.text["enter"]["text"]
        else:
            return NLG.enter_room(self.name)

    def cannot_enter(self, reason: str = None) -> str:
        """Method when not entering a room"""
        return NLG.cannot_move(self.name, reason)
    
    def visibility(self) -> str:
        """Method when triggering visibility text"""
        if State.torch_lit or State.get_player().character.has_darkvision(): 
            OutputBuilder.append(self.text["visibility"]["text"])
            self.text["visibility"]["read"] = True
    
    def trigger(self) -> str:
        """Method to print any new text if conditions met"""
        for text_type in self.text:
            if not self.text[text_type]["read"]:
                # execute function
                if text_type in self.text:
                    self.text[text_type]["trigger"]()
                    
