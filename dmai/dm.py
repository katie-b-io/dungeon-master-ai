from dmai.game.state import State
from dmai.game.adventure import Adventure
from dmai.domain.actions import Actions
from dmai.nlg.nlg import NLG
from dmai.game.npcs.npc_collection import NPCCollection
import dmai

class DM:

    # class variables
    utter_type_map = {"name": NLG.acknowledge_name, "action": NLG.get_action, "start": NLG.enter_room}
    ENTITY_CONFIDENCE = 0.75

    def __init__(self, adventure: str) -> None:
        """Main DM class"""
        self._dm_utter = None
        self._player_utter = None
        self.adventure = Adventure(adventure)

        # Initialise the state with the adventure data
        State.set_adventure(self.adventure)
        
        # Initialise the NPC Collection with the adventure data
        self.npcs = NPCCollection(self.adventure)
        
        # Initialise the actions with the adventure and npc data
        self.actions = Actions(self.adventure, self.npcs)

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
            if utter_type == "start":
                self._start_game()
            else:
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

    def _start_game(self) -> None:
        """Start the game"""
        starting_room = State.get_current_room_id()
        self._generate_utterance(utter_type="start", kwargs={"room": starting_room, "adventure": self.adventure})
        State.start()
        
    def _generate_utterance(self, utter: str = None, utter_type: str = None, kwargs: dict = {}) -> str:
        """Generate an utterance for the player"""
        if utter:
            self._dm_utter = utter
        elif not utter_type:
            self._dm_utter = NLG.get_action()
        else:
            try:
                self._dm_utter = self.utter_type_map[utter_type](**kwargs)
            except KeyError as e:
                print("Utterance type does not exist: {e}".format(e=e))
                self._dm_utter = NLG.get_action()

    def get_intro_text(self) -> str:
        return self.adventure.intro_text

    def _get_destination(self, nlu_entities: dict) -> str:
        """Extract a destination from NLU entities dictionary.
        Returns a string with destination"""
        for entity in nlu_entities:
            if entity["entity"] == "location" and entity["confidence"] >= self.ENTITY_CONFIDENCE:
                return entity["value"]

    def _get_target(self, nlu_entities: dict) -> str:
        """Extract a target from NLU entities dictionary.
        Returns a string with destination"""
        monster = None
        i = None
        npc = None
        for entity in nlu_entities:
            if entity["entity"] == "monster" and entity["confidence"] >= self.ENTITY_CONFIDENCE:
                monster = entity["value"]
            if entity["entity"] == "id" and entity["confidence"] >= self.ENTITY_CONFIDENCE:
                i = entity["value"]
            if entity["entity"] == "npc" and entity["confidence"] >= self.ENTITY_CONFIDENCE:
                npc = entity["value"]
                
        # monsters are indexed by a unique id, determine it if possible
        if monster:
            if i:
                # player appeared to specify particular individual, get it's id
                monster_id = "{m}_{i}".format(m=monster, i=i)
            else:
                # player hasn't appeared to specify particular individual, pick first alive one
                # TODO get player confirmation about which monster to target
                monster_id = self.npcs.get_monster_id(monster, status="alive", location=State.get_current_room_id())
            return monster_id
        
        # NPCs have unique ids
        if npc:
            return npc
        
    def move(self, destination: str = None, entity: str = None, nlu_entities: dict = None) -> bool:
        """Attempt to move an entity to a destination determined by NLU or specified.
        Returns whether the move was successful."""
        if not entity:
            entity = "player"
        if not destination and nlu_entities:
            destination = self._get_destination(nlu_entities)
            
        print("Moving {e} to {d}!".format(e=entity, d=destination))
        (moved, utterance) = self.actions.move(entity, destination)
        self._generate_utterance(utter=utterance)
        return moved

    def attack(self, target: str = None, attacker: str = None, nlu_entities: dict = None) -> bool:
        """Attempt an attack by attacker against target determined by NLU or specified.
        Returns whether the attack was successful."""
        
        if not attacker:
            attacker = "player"
        if not target and nlu_entities:
            target = self._get_target(nlu_entities)
        
        if not target:
            attacked = False
            utterance = NLG.no_target()
        else:
            print("{a} is attacking {t}!".format(a=attacker, t=target))
            (attacked, utterance) = self.actions.attack(attacker, target)
        self._generate_utterance(utter=utterance)
        return attacked