import inflect
engine = inflect.engine()

from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class Roleplay(Action):
    def __init__(
        self,
        verb: str,
        target: str,
        target_type: str,
        player_utter: str,
        state: State,
        output_builder: OutputBuilder,
    ) -> None:
        """Roleplay class"""
        Action.__init__(self)
        self.verb = verb
        self.target = target
        self.target_type = target_type
        self.player_utter = player_utter
        self.state = state
        self.output_builder = output_builder

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._roleplay()

    def _can_roleplay(self) -> tuple:
        """Check if roleplay can happen.
        Returns tuple (bool, str) to indicate whether roleplay is possible
        and reason why not if not."""

        # check if player and target are within range
        try:
            current = self.state.get_current_room()

            if self.target_type == "monster" or self.target_type == "npc":
                if (current != self.state.get_current_room(self.target)):
                    return (False, "different location")

            # can't roleplay if can't see
            if not current.visibility:
                if (
                    not self.state.torch_lit
                    and not self.state.get_player().character.has_darkvision()
                ):
                    return (False, "no visibility")

            # none of the above situations were triggered so allow roleplay
            return (True, "")
        except UnrecognisedEntityError:
            return (False, "unknown entity")

    def _roleplay(self) -> bool:
        """Attempt to roleplay.
        Returns a bool to indicate whether the action was successful"""

        # check if roleplay can happen
        (roleplay, reason) = self._can_roleplay()
        if roleplay:
            # if entity is monster or npc
            if self.target_type == "monster" or self.target_type == "npc":
                self.output_builder.append(NLG.roleplay(verb=self.verb, target=self.target, player_utter=self.player_utter))
            elif self.target_type:
                # check description of room to see if target's here
                room_desc = self.state.get_current_room().get_all_text_array()
                plural_target = engine.plural(self.target)
                if self.target in room_desc or plural_target in room_desc:
                    self.output_builder.append(NLG.roleplay(verb=self.verb, target=self.target, player_utter=self.player_utter))
                else:
                    self.output_builder.append(NLG.roleplay(verb=self.verb, target=self.target, player_utter=self.player_utter, failure=True))
            
            else:
                self.output_builder.append(NLG.roleplay(verb=self.verb))

        else:
            self.output_builder.append(
                NLG.cannot_roleplay(self.verb, self.target, reason)
            )
            if self.state.get_player().agent.get_next_move():
                self.state.nag_player()
        return roleplay
