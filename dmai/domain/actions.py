from dmai.utils.output_builder import OutputBuilder
from dmai.game.npcs.npc_collection import NPCCollection
from dmai.utils.loader import Loader
from dmai.utils.exceptions import UnrecognisedRoomError
from dmai.game.state import State
from dmai.game.adventure import Adventure
from dmai.nlg.nlg import NLG
import dmai


class Actions:

    # class variables
    action_data = dict()

    def __init__(self, adventure: Adventure, npcs: NPCCollection) -> None:
        """Actions class"""
        self.adventure = adventure
        self.npcs = npcs
        self.actions = dict()
        self._load_action_data()

    def __repr__(self) -> str:
        return "Actions:\n{a}".format(a=self.actions)

    @classmethod
    def _load_action_data(cls) -> None:
        """Set the cls.action_data class variable data"""
        cls.action_data = Loader.load_json("data/domain/actions.json")

    def _can_move(self, entity: str, destination: str) -> tuple:
        """Check if an entity can be moved to a specified destination.
        Returns tuple (bool, str) to indicate whether movement is possible
        and reason why not if not."""

        # check if destination is accessible
        current = State.get_current_room_id(entity)

        if current == destination:
            return (False, "same")

        try:
            if State.travel_allowed(current, destination):
                return (True, "")
            else:
                return (False, "locked")
        except UnrecognisedRoomError:
            raise

    def move(self, entity: str, destination: str) -> tuple:
        """Attempt to move an entity to the specified destination.
        Returns a tuple with the action status and room enter/cannot_enter text."""

        # check if entity can move
        (can_move, reason) = self._can_move(entity, destination)
        if can_move:
            State.set_current_room(entity, destination)
            utterance = self.adventure.get_room(destination).enter()
        else:
            utterance = self.adventure.get_room(destination).cannot_enter(reason)
        return (can_move, utterance)

    def _can_attack(self, attacker: str, target: str) -> tuple:
        """Check if a target can be attacked by an attacker.
        Returns tuple (bool, str) to indicate whether attack is possible
        and reason why not if not."""
        
        # check if attacker and target are within attack range
        if not State.get_current_room(attacker) == State.get_current_room(target):
            return (False, "Different location")
        return (True, "")

    def attack(self, attacker: str, target: str) -> tuple:
        """Attempt to attack a specified target.
        Returns a tuple with the attack status and attack resolution text."""

        # check if attack can happen
        (can_attack, reason) = self._can_attack(attacker, target)
        if can_attack:
            # check if target will end game
            if self.npcs.get_type(target) == "npc":
                if self.npcs.get_npc(target).attack_ends_game:
                    # this is a game end condition
                    OutputBuilder.append(NLG.attack_npc_end_game(target))
                    dmai.dmai_helpers.gameover()
                
            utterance = "{a} attacked {t}!".format(a=attacker, t=target)
            State.combat()
            return (can_attack, utterance)
        else:
            utterance ="{a} can't attack {t}!\n{r}".format(a=attacker, t=target, r=reason)
            return (can_attack, utterance)
