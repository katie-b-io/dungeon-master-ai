from dmai.game import State, Adventure
from dmai.domain import Domain, Actions
from dmai.domain.characters import Character
from dmai.nlg import NLG


class DM:

    # class variables
    utter_type_map = {"name": NLG.acknowledge_name, "action": NLG.get_action}

    def __init__(self, adventure: str) -> None:
        """Main DM class"""
        self.dm_utter = None
        self.player_utter = None
        self.domain = Domain()
        self.adventure = Adventure(adventure)

        # Load the domain data
        self.domain.load_all()

        # Build the adventure world
        self.adventure.build_world()

        # Initialise the state with the adventure data
        self.state = State(self.adventure)

        # Initialise the actions with the state and adventure data
        self.actions = Actions(self.state, self.adventure)

        # Initialise the player intent map
        self.player_intent_map = {"move": self.move}

    def input(
        self,
        player_utter: str,
        utter_type: str = None,
        intent: str = None,
        kwargs: dict = {},
    ) -> None:
        """Receive a player input"""
        self.player_utter = player_utter
        if utter_type:
            self._generate_utterance(utter_type=utter_type)
        if intent:
            # look up intent in map
            try:
                self.player_intent_map[intent](**kwargs)
            except KeyError:
                print("Intent not in map: {i}".format(i=intent))
                raise

    @property
    def output(self) -> str:
        """Return an output for the player"""
        return self.dm_utter

    def _generate_utterance(self, utter: str = None, utter_type: str = None) -> str:
        """Generate an utterance for the player"""
        if utter:
            self.dm_utter = utter
        elif not utter_type:
            self.dm_utter = NLG.get_action()
        else:
            try:
                self.dm_utter = self.utter_type_map[utter_type]()
            except KeyError as e:
                print("Utterance type does not exist: {e}".format(e=e))
                self.dm_utter = NLG.get_action()

    def get_intro_text(self) -> str:
        return self.adventure.intro_text

    def get_character(self, character: str) -> Character:
        return self.domain.get_character(character)

    def move(self, destination: str, entity: str = None) -> str:
        """Attempt to move an entity to a specified destination.
        Return a string with the utterance to output to the players"""
        if not entity:
            entity = "player"
        print("Moving {e} to {d}!".format(e=entity, d=destination))
        self._generate_utterance(utter=self.actions.move(entity, destination))
