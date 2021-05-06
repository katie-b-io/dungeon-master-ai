from dmai.game import Adventure
from dmai.utils import Loader
from dmai.game import State, Adventure


class Actions:

    # class variables
    action_data = dict()

    def __init__(self, state: State, adventure: Adventure) -> None:
        """Actions class"""
        self.state = state
        self.adventure = adventure
        self.actions = dict()
        self._load_action_data()

    def __repr__(self) -> str:
        return "Actions:\n{a}".format(a=self.actions)

    @classmethod
    def _load_action_data(self) -> None:
        """Set the self.action_data class variable data"""
        self.action_data = Loader.load_json("data/actions.json")

    def _can_move(self, entity: str, destination: str) -> tuple:
        """Check if an entity can be moved to a specified destination.
        Returns boolean to indicate whether movement was successful."""

        # check if destination is accessible
        current = self.state.get_current_room_id(entity)

        if current == destination:
            return (False, "same")

        if self.state.travel_allowed(current, destination):
            return (True, "")
        else:
            return (False, "locked")

    def move(self, entity: str, destination: str) -> str:
        """Attempt to move an entity to the specified destination.
        Returns the room enter/cannot_enter text."""

        # check if entity can move
        (can_move, reason) = self._can_move(entity, destination)
        if can_move:
            self.state.set_current_room(entity, destination)
            return self.adventure.get_room(destination).enter(reason)
        else:
            return self.adventure.get_room(destination).cannot_enter(reason)
