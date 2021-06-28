from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.domain.actions.action import Action
import dmai


class PickUp(Action):
    def __init__(self, item: str, entity: str) -> None:
        """PickUp class"""
        Action.__init__(self)
        self.item = item
        self.entity = entity

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def execute(self, **kwargs) -> bool:
        return self._pick_up()

    def _can_pick_up(self) -> tuple:
        """Check if an item can be picked up by an entity.
        Returns tuple (bool, str) to indicate whether pick up is possible
        and reason why not if not."""

        # check if entity and item are within pick up range
        try:
            current = State.get_current_room(self.entity)
            if not current.has_item(self.item):
                return (False, "not in room")

            # can't pick up if can't see
            if not current.visibility:
                if self.entity == "player":
                    if (
                        not State.torch_lit
                        or State.get_player().character.has_darkvision()
                    ):
                        return (False, "no visibility")

            # none of the above situations were triggered so allow pick up
            return (True, "")
        except UnrecognisedEntityError:
            return (False, "unknown entity")

    def _pick_up(self) -> bool:
        """Attempt to pick up a specified item.
        Returns a bool to indicate whether the action was successful"""

        # check if pick up can happen
        (picked_up, reason) = self._can_pick_up()
        if picked_up:
            # TODO check if picking up item will end game
            # OutputBuilder.append(State.get_dm().get_bad_ending())
            # dmai.dmai_helpers.gameover()
            picked_up = State.get_item_collection().add_item(self.item)
            if picked_up:
                State.get_current_room(self.entity).took_item(self.item)
                OutputBuilder.append(
                    NLG.pick_up(State.get_item_collection().get_name(self.item))
                )
            return picked_up
        else:
            OutputBuilder.append(
                NLG.cannot_pick_up(
                    State.get_item_collection().get_name(self.item), reason
                )
            )
            return picked_up
