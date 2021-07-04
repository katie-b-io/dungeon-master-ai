from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError, UnrecognisedRoomError
from dmai.utils.text import Text
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class Investigate(Action):
    def __init__(self, target: str, target_type: str = "") -> None:
        """Investigate class"""
        Action.__init__(self)
        self.target = target
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
            current = State.get_current_room()
            if not current.visibility:
                if (
                    not State.torch_lit
                    and not State.get_player().character.has_darkvision()
                ):
                    return (False, "no visibility")

            # check if target is in same location as player
            if (
                not State.get_current_room_id(self.target)
                == State.get_current_room_id()
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
            if State.get_entity_name(self.target):
                target = State.get_entity_name(self.target)
            else:
                target = self.target
            OutputBuilder.append(NLG.cannot_investigate(target, reason))
            return can_investigate

        # if the entity is scenery, return a failsafe utterance
        if self.target_type == "scenery":
            # check the description of the room to see if it's here first
            room_desc = State.get_current_room().text["enter"]["text"]
            room_desc = room_desc.lower().replace(".", "").replace(",", "").split(" ")
            if self.target in room_desc:
                OutputBuilder.append(
                    "You examine the {t}, but you see nothing special.".format(
                        t=self.target
                    )
                )
            else:
                OutputBuilder.append(
                    "I don't think I mentioned anything about {t}. Maybe you could {h}".format(
                        t=self.target, h=State.get_player().agent.get_next_move()
                    )
                )
            return True

        if self.target_type == "drink":
            if State.get_current_room().ale:
                OutputBuilder.append("You see a wonderful selection of ales.")
                return True
            else:
                OutputBuilder.append("Unfortunately, there are no ales here.")
                return True

        if self.target_type == "puzzle":
            OutputBuilder.append("Trigger the puzzle checks")
            State.get_current_room().puzzles.get_puzzle(self.target).investigate_trigger()
            return True

        if self.target_type == "door":
            try:
                target = State.get_room_name(self.target)
            except UnrecognisedRoomError:
                target = self.target
            if target == "door":
                OutputBuilder.append("It's just a door.")
            else:
                OutputBuilder.append("This door goes to the {t}.".format(t=target))
            return True

        if can_investigate:
            State.explore()
            State.clear_skill_check()
            if self.target_type == "npc":
                description = State.get_entity(self.target).description
                OutputBuilder.append(description)
            elif self.target_type == "monster":
                monster = State.get_entity(self.target)
                if not State.is_alive(self.target):
                    if monster.treasure:
                        t = []
                        for treasure in monster.treasure:
                            State.get_player().character.items.add_item(treasure)
                            t.append(
                                State.get_player().character.items.get_name(treasure)
                            )
                        description = "{d} It's dead. You find {t} on them, which you add to your inventory.".format(
                            d=monster.description, t=Text.properly_format_list(t)
                        )
                    else:
                        description = "{d} It's dead.".format(d=monster.description)
                else:
                    description = "{d} It's alive.".format(d=monster.description)
                OutputBuilder.append(description)
            else:
                OutputBuilder.append(
                    "You investigate {t} but see nothing significant.".format(
                        t=self.target
                    )
                )
        else:
            OutputBuilder.append(NLG.cannot_investigate(self.target, reason))
        return can_investigate
