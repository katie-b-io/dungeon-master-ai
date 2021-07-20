import inflect
engine = inflect.engine()

from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError
from dmai.utils.text import Text
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
from dmai.utils.logger import get_logger

logger = get_logger(__name__)



class Investigate(Action):
    def __init__(self, target: str, state: State, output_builder: OutputBuilder, target_type: str = "") -> None:
        """Investigate class"""
        Action.__init__(self)
        self.target = target
        self.state = state
        self.output_builder = output_builder
        self.target_type = target_type

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._investigate()

    def _can_investigate(self) -> tuple:
        """Check if player can investigate target.
        Returns tuple (bool, str) to indicate whether investigation is possible
        and reason why not if not."""
        try:
            # check for visibility
            current = self.state.get_current_room()
            if not current.visibility:
                if (
                    not self.state.torch_lit
                    and not self.state.get_player().character.has_darkvision()
                ):
                    return (False, "no visibility")

            # check if target is in same location as player
            if (
                not self.state.get_current_room_id(self.target)
                == self.state.get_current_room_id()
            ):
                return (False, "different location")

            return (True, "")
        except UnrecognisedEntityError:
            return (False, "unknown entity")

    def _investigate(self) -> bool:
        """Attempt to investigate current location.
        Returns a bool to indicate whether the action was successful"""

        # check if entity can investigate target
        (can_investigate, reason) = self._can_investigate()
        if reason == "no visibility":
            if self.state.get_entity_name(self.target):
                target = self.state.get_entity_name(self.target)
            else:
                target = self.target
            self.output_builder.append(NLG.cannot_investigate(target, reason))
            return can_investigate

        # if the entity is scenery, return a failsafe utterance
        if self.target_type == "scenery":
            # check the description of the room to see if it's here first
            room_desc = self.state.get_current_room().get_all_text_array()
            plural_target = engine.plural(self.target)
            if self.target in room_desc or plural_target in room_desc:
                self.output_builder.append(
                    "You examine the {t}, but you see nothing special.".format(
                        t=self.target
                    )
                )
            else:
                self.output_builder.append(
                    "I don't think I mentioned anything about {t}.".format(t=self.target)
                )
                if self.state.get_player().agent.get_next_move():
                    self.state.nag_player()
                    
            return True

        if self.target_type == "drink":
            if self.state.get_current_room().ale:
                self.output_builder.append("You see a wonderful selection of ales.")
                return True
            else:
                self.output_builder.append("Unfortunately, there are no ales here.")
                return True

        if self.target_type == "puzzle":
            puzzle = self.state.get_current_room().puzzles.get_puzzle(self.target)
            if puzzle:
                if hasattr(puzzle, "description"):
                    self.output_builder.append(puzzle.description)
                puzzle.investigate_trigger()
                return True

        if self.target_type == "door":
            try:
                target = self.state.get_room_name(self.target)
            except UnrecognisedRoomError:
                target = self.target
                self.output_builder.append("I'm not sure what door you want to investigate.")
                return False

            if target == "door":
                self.output_builder.append("It's just a door.")
            else:
                self.output_builder.append("This door goes to the {t}.".format(t=target))
                room = self.state.get_current_room()
                puzzle_id = "{r1}---{r2}".format(r1=room.id, r2=self.target)
                puzzle = room.puzzles.get_puzzle(puzzle_id)
                if puzzle:
                    if puzzle.id not in self.state.solved_puzzles:
                        if "describe" in puzzle.investigate:
                            self.output_builder.append(puzzle.investigate["describe"]["say"])
            return True
        
        if self.target_type == "item":
            item_collection = self.state.get_player().character.items
            if item_collection.has_item(self.target)[0]:
                self.output_builder.append(item_collection.get_item(self.target).description)
                return True

        if can_investigate:
            self.state.explore()
            self.state.clear_skill_check()
            if self.target_type == "npc":
                description = self.state.get_entity(self.target).description
                self.output_builder.append(description)
            elif self.target_type == "monster":
                monster = self.state.get_entity(self.target)
                if not self.state.is_alive(self.target):
                    if self.state.monster_treasure_map[monster.unique_id]:
                        t = []
                        for treasure in self.state.monster_treasure_map[monster.unique_id]:
                            self.state.get_player().character.items.add_item(treasure)
                            monster.took_item(treasure)
                            t.append(
                                self.state.get_player().character.items.get_name(treasure)
                            )
                        description = "{d} It's dead. You find {t} on them, which you add to your inventory.".format(
                            d=monster.description, t=Text.properly_format_list(t)
                        )
                    else:
                        description = "{d} It's dead.".format(d=monster.description)
                else:
                    description = "{d} It's alive.".format(d=monster.description)
                self.output_builder.append(description)
            else:
                self.output_builder.append(
                    "You investigate {t} but see nothing significant.".format(
                        t=self.target
                    )
                )
        else:
            self.output_builder.append(NLG.cannot_investigate(self.target, reason))
        return can_investigate
