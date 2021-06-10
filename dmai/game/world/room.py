from dmai.game.world.puzzles.puzzle_collection import PuzzleCollection
from dmai.game.world.puzzles.puzzle_collection import PuzzleCollection
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

            # replace the attributes values with objects where appropriate
            self.puzzles = PuzzleCollection(self.puzzles)
            
        except AttributeError as e:
            logger.error("Cannot create room, incorrect attribute: {e}".format(e=e))
            raise
        
        trigger_map = {
            "enter": self.enter,
            "exit": print,
            "visibility": self.visibility
        }
        
        # populate the self.text object
        for text_type in self.text:
            text = self.text[text_type]
            self.text[text_type] = {
                "text": text,
                "can_trigger": True,
                "trigger": trigger_map[text_type]
            }

    def __repr__(self) -> str:
        return "Room: {a}".format(a=self.name)

    def enter(self) -> None:
        """Method when entering a room"""
        logger.debug("Triggering enter in room: {r}".format(r=self.id))
        if not State.stationary:
            if not self.visited:
                self.visited = True
                OutputBuilder.append(self.text["enter"]["text"])
            else:
                OutputBuilder.append(NLG.enter_room(self.name))
            State.halt()
    
    def visibility(self) -> str:
        """Method when triggering visibility text"""
        logger.debug("Triggering visibility in room: {r}".format(r=self.id))
        if State.torch_lit or State.get_player().character.has_darkvision(): 
            OutputBuilder.append(self.text["visibility"]["text"])
            self.text["visibility"]["can_trigger"] = False
    
    def trigger(self) -> None:
        """Method to print any new text if conditions met"""
        for text_type in self.text:
            if self.text[text_type]["can_trigger"]:
                # execute function
                if text_type in self.text:
                    self.text[text_type]["trigger"]()
                    
    def get_connected_rooms(self) -> list:
        """Method to return the connected rooms"""
        return list(self.connections.keys())