from dmai.game import State, Adventure
from dmai.domain import Actions
from dmai.domain.characters import Character, CharacterCollection
from dmai.domain.monsters import MonsterCollection
from dmai.nlg import NLG


class DM:

    # class variables
    utter_type_map = {"name": NLG.acknowledge_name, "action": NLG.get_action}

    def __init__(self, adventure: str) -> None:
        """Main DM class"""
        self._dm_utter = None
        self._player_utter = None
        self.monsters = MonsterCollection()
        self.characters = CharacterCollection()
        self.adventure = Adventure(adventure)

        # Build the adventure world
        self.adventure.build_world()

        # Initialise the state with the adventure data
        self.state = State(self.adventure)

        # Initialise the actions with the state and adventure data
        self.actions = Actions(self.state, self.adventure)

        # Initialise the player intent map
        self.player_intent_map = {"move": self.move, "attack": self.attack}

    def input(
        self,
        player_utter: str,
        utter_type: str = None,
        intent: str = None,
        kwargs: dict = {},
    ) -> bool:
        """Receive a player input.
        Returns whether the utterance was successful."""
        self._player_utter = player_utter
        if utter_type:
            self._generate_utterance(utter_type=utter_type)
            return True
        if intent:
            # look up intent in map
            try:
                return self.player_intent_map[intent](**kwargs)
            except KeyError:
                print("Intent not in map: {i}".format(i=intent))
                raise
        return True

    @property
    def output(self) -> str:
        """Return an output for the player"""
        return self._dm_utter

    def _generate_utterance(self, utter: str = None, utter_type: str = None) -> str:
        """Generate an utterance for the player"""
        if utter:
            self._dm_utter = utter
        elif not utter_type:
            self._dm_utter = NLG.get_action()
        else:
            try:
                self._dm_utter = self.utter_type_map[utter_type]()
            except KeyError as e:
                print("Utterance type does not exist: {e}".format(e=e))
                self._dm_utter = NLG.get_action()

    def get_intro_text(self) -> str:
        return self.adventure.intro_text

    def get_character(self, character: str) -> Character:
        return self.characters.get_character(character)

    def move(self, destination: str, entity: str = None) -> bool:
        """Attempt to move an entity to a specified destination.
        Returns whether the move was successful."""
        if not entity:
            entity = "player"
        print("Moving {e} to {d}!".format(e=entity, d=destination))
        (moved, utterance) = self.actions.move(entity, destination)
        self._generate_utterance(utter=utterance)
        return moved
