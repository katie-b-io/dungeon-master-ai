from dmai.utils.output_builder import OutputBuilder
from dmai.game.state import State
from dmai.game.adventure import Adventure
from dmai.domain.actions.actions import Actions
from dmai.nlg.nlg import NLG
from dmai.nlu.nlu import NLU
from dmai.game.npcs.npc_collection import NPCCollection
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class DM:

    # class variables
    ENTITY_CONFIDENCE = 0.5

    def __init__(self, adventure: str, nlu: NLU, state: State, output_builder: OutputBuilder) -> None:
        """Main DM class"""
        self.nlu = nlu
        self._dm_utter = None
        self._player_utter = None
        self.triggers = []
        self.state = state
        self.output_builder = output_builder
        self.adventure = Adventure(adventure, self.state, self.output_builder)

    def load(self) -> None:
        # Initialise the NPC Collection with the adventure data
        self.npcs = NPCCollection(self.adventure, self.state, self.output_builder)
        self.npcs.load()

        # Initialise the actions with the adventure and npc data
        self.actions = Actions(self.adventure, self.npcs, self.state, self.output_builder)

        # Initialise the player intent map
        self.player_intent_map = {
            "no_intent": {
                "name": "no intent",
                "desc": "couldn't determine intent",
                "func": self.no_intent
            },
            "hint": {
                "name": "hint",
                "desc": "ask for a hint",
                "func": self.hint
            },
            "move": {
                "name": "move",
                "desc": "move to another room",
                "func": self.move,
                },
            "attack": {
                "name": "attack",
                "desc": "attack a target",
                "func": self.attack,
                },
            "use": {
                "name": "use",
                "desc": "use equipment",
                "func": self.use,
                },
            "stop_using": {
                "name": "stop using",
                "desc": "stop using equipment",
                "func": self.stop_using,
                },
            "equip": {
                "name": "equip",
                "desc": "equip weapon",
                "func": self.equip,
                },
            "unequip": {
                "name": "unequip",
                "desc": "unequip weapon",
                "func": self.unequip,
                },
            "converse": {
                "name": "converse",
                "desc": "converse with an NPC",
                "func": self.converse,
                },
            "affirm": {
                "name": "affirm",
                "desc": "respond with an affirmation",
                "func": self.affirm,
                },
            "deny": {
                "name": "deny",
                "desc": "respond with a denial",
                "func": self.deny,
                },
            "explore": {
                "name": "explore",
                "desc": "explore your surroundings",
                "func": self.explore,
                },
            "roll": {
                "name": "roll",
                "desc": "roll some dice",
                "func": self.roll,
                },
            "pick_up": {
                "name": "pick up",
                "desc": "pick up an item",
                "func": self.pick_up
            },
            "health": {
                "name": "health",
                "desc": "get health status",
                "func": self.health
            },
            "inventory": {
                "name": "inventory",
                "desc": "get inventory status",
                "func": self.inventory
            },
            "force": {
                "name": "force",
                "desc": "force open",
                "func": self.force
            },
            "ability_check": {
                "name": "ability check",
                "desc": "perform ability check",
                "func": self.ability_check
            },
            "skill_check": {
                "name": "skill check",
                "desc": "perform skill check",
                "func": self.skill_check
            },
            "ale": {
                "name": "ale",
                "desc": "drink ale",
                "func": self.ale
            },
            "roleplay": {
                "name": "roleplay",
                "desc": "roleplay",
                "func": self.roleplay
            },
            "negotiate": {
                "name": "negotiate",
                "desc": "negotiate",
                "func": self.negotiate
            },
            "rescue": {
                "name": "rescue",
                "desc": "rescue",
                "func": self.rescue
            },
            "bot_challenge": {
                "name": "bot_challenge",
                "desc": "challenge the AI",
                "func": self.bot_challenge
            },
            "stealth": {
                "name": "stealth",
                "desc": "stealth",
                "func": self.stealth
            },
            "pick_lock": {
                "name": "pick_lock",
                "desc": "pick a lock",
                "func": self.pick_lock
            }
        }

    def input(
        self,
        player_utter: str,
        utter_type: str = None,
        intent: str = None,
        kwargs: dict = {},
    ) -> bool:
        """Receive a player input.
        Returns whether the utterance was successful."""
        succeed = False
        self._player_utter = player_utter
        if utter_type:
            if utter_type == "name":
                self.output_builder.append(NLG.acknowledge_name(self.state.char_name))
            else:
                self.output_builder.append(NLG.get_action(self.state.char_name))
            succeed = True

        elif intent:
            # look up intent in map
            try:
                succeed = self.player_intent_map[intent]["func"](**kwargs)
            except KeyError:
                logger.error("(SESSION {s}) Intent not in map: {i}".format(s=self.state.session.session_id, i=intent))
                raise

        # execute any triggers
        if succeed:
            self.execute_triggers()

        # prepare next AI moves
        self.state.get_player().prepare_next_move()

        # prepare next monster moves
        for monster in self.npcs.get_all_monsters():
            if self.state.is_alive(monster.unique_id):
                if self.state.get_current_room_id() == self.state.get_current_room_id(
                    monster.unique_id
                ):
                    monster.prepare_next_move()

        # last thing to do: maintain state
        self.state.maintenance()

        return succeed

    @property
    def output(self) -> str:
        """Return an output for the player"""
        if self.output_builder.has_response():
            return self.output_builder.format()
        else:
            return NLG.get_action(self.state.char_name)

    def register_trigger(self, trigger: object) -> None:
        """Register a trigger object"""
        if trigger not in self.triggers:
            logger.debug("(SESSION {s}) Registering trigger: {n}".format(s=self.state.session.session_id, n=str(trigger)))
            self.triggers.append(trigger)

    def deregister_trigger(self, trigger: object) -> None:
        """Deregister a trigger object"""
        if trigger in self.triggers:
            logger.debug("(SESSION {s}) Deregistering trigger: {n}".format(s=self.state.session.session_id, n=str(trigger)))
            self.triggers.remove(trigger)

    def execute_triggers(self) -> None:
        """Method to execute triggers"""
        for obj in self.triggers:
            obj.trigger()

    def get_intro_text(self) -> str:
        return self.adventure.intro_text
    
    def get_good_ending(self) -> str:
        return self.adventure.text["conclusion"]["good_ending"]
    
    def get_bad_ending(self) -> str:
        return self.adventure.text["conclusion"]["bad_ending"]

    def _get_destination(self, nlu_entities: dict) -> str:
        """Extract a destination from NLU entities dictionary.
        Returns a string with destination"""
        for entity in nlu_entities:
            if (
                entity["entity"] == "location"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                return ("location", entity["value"])
            
            (target_type, target) = self._get_target(nlu_entities)
            if target and (target_type == "npc" or target_type == "monster"):
                return ("location", self.state.get_current_room_id(target))
        return (None, None)

    def _get_noun(self, nlu_entities: dict) -> tuple:
        """Extract any entity from NLU entities dictionary"""
        for func in [
                self._get_target,
                self._get_equipment,
                self._get_weapon,
                self._get_item,
                self._get_drink
            ]:
            if func == self._get_target:
                (target_type, target) = func(nlu_entities, monster_status=None)
            else:
                (target_type, target) = func(nlu_entities)
            if target:
                return (target_type, target)
        return (None, None)

    def _get_target(self, nlu_entities: dict, monster_status: str = "alive") -> tuple:
        """Extract a target from NLU entities dictionary.
        Returns tuple with the type of target and a string with target ID"""
        monster = None
        i = None
        npc = None
        door = False
        location = None
        puzzle = None
        scenery = None
        for entity in nlu_entities:
            if (
                entity["entity"] == "monster"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                monster = entity["value"]
            if (
                entity["entity"] == "id"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                i = entity["value"]
            if (
                entity["entity"] == "npc"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                npc = entity["value"]
            if (
                entity["entity"] == "door"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                door = True
            if (
                entity["entity"] == "location"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                location = entity["value"]
            if (
                entity["entity"] == "puzzle"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                puzzle = entity["value"]
            if (
                entity["entity"] == "scenery"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                scenery = entity["value"]
        
        # return the door and location
        if door:
            if location:
                return ("door", location)
            else:
                return ("door", "door")
        
        # return the puzzle
        if puzzle:
            return ("puzzle", puzzle)
        
        # return the scenery
        if scenery:
            return ("scenery", scenery)
        
        # return the location
        if location:
            return ("location", location)

        # monsters are indexed by a unique id, determine it if possible
        if monster:
            if i:
                # player appeared to specify particular individual, get it's id
                monster_id = "{m}_{i}".format(m=monster, i=i)
            else:
                # player hasn't appeared to specify particular individual, pick first alive one
                monster_id = self.npcs.get_monster_id(
                    monster, status=monster_status, location=self.state.get_current_room_id()
                )
            return ("monster", monster_id)

        # NPCs have unique ids
        if npc:
            return ("npc", npc)

        return (None, None)

    def _get_entity(self, nlu_entities: dict, monster_status: str = "alive") -> tuple:
        """Extract a entity from NLU entities dictionary.
        Returns tuple with the type of entity and a string with entity ID"""
        monster = None
        i = None
        npc = None
        for entity in nlu_entities:
            if (
                entity["entity"] == "monster"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                monster = entity["value"]
            if (
                entity["entity"] == "id"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                i = entity["value"]
            if (
                entity["entity"] == "npc"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                npc = entity["value"]

        # monsters are indexed by a unique id, determine it if possible
        if monster:
            if i:
                # player appeared to specify particular individual, get it's id
                monster_id = "{m}_{i}".format(m=monster, i=i)
            else:
                # player hasn't appeared to specify particular individual, pick first alive one
                monster_id = self.npcs.get_monster_id(
                    monster, status=monster_status, location=self.state.get_current_room_id()
                )
            return ("monster", monster_id)

        # NPCs have unique ids
        if npc:
            return ("npc", npc)

        return (None, None)

    def _get_npc(self) -> str:
        """Get an NPC.
        Returns a string with NPC ID"""
        for npc in self.npcs.get_all_npc_ids():
            if self.state.get_current_room_id() == self.state.get_current_room_id(npc):
                return ("npc", npc)
        return (None, None)

    def _get_equipment(self, nlu_entities: dict) -> str:
        """Extract a equipment from NLU entities dictionary.
        Returns a string with equipment"""
        for entity in nlu_entities:
            if (
                entity["entity"] == "equipment"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                return ("equipment", entity["value"])
        return (None, None)

    def _get_weapon(self, nlu_entities: dict) -> str:
        """Extract a weapon from NLU entities dictionary.
        Returns a string with weapon"""
        for entity in nlu_entities:
            if (
                entity["entity"] == "weapon"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                return ("weapon", entity["value"])
        return (None, None)

    def _get_die(self, nlu_entities: dict) -> str:
        """Extract a die from NLU entities dictionary.
        Returns a string with die"""
        for entity in nlu_entities:
            if (
                entity["entity"] == "die"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                return ("die", entity["value"])
        return ("die", None)
    
    def _get_item(self, nlu_entities: dict) -> str:
        """Extract an item from NLU entities dictionary.
        Returns a string with item"""
        for entity in nlu_entities:
            if (
                entity["entity"] == "item"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                return ("item", entity["value"])
        return (None, None)

    def _get_scenery(self, nlu_entities: dict) -> str:
        """Extract scenery from NLU entities dictionary.
        Returns a string with scenery"""
        for entity in nlu_entities:
            if (
                entity["entity"] == "scenery"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                return ("scenery", entity["value"])
        return (None, None)

    def _get_door(self, nlu_entities: dict) -> str:
        """Extract door from NLU entities dictionary.
        Returns a string with door"""
        door = False
        location = None
        for entity in nlu_entities:
            if (
                entity["entity"] == "door"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                door = True
            if (
                entity["entity"] == "location"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                location = entity["value"]
            
        # return the door and location
        if door:
            if location:
                return ("door", location)
            else:
                return ("door", "door")

        return (None, None)

    def _get_drink(self, nlu_entities: dict) -> str:
        """Extract a drink from NLU entities dictionary.
        Returns a string with item"""
        for entity in nlu_entities:
            if (
                entity["entity"] == "drink"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                return ("drink", entity["value"])
        return (None, None)

    def _get_verb(self, nlu_entities: dict) -> str:
        """Extract a verb from NLU entities dictionary.
        Returns a string with item"""
        for entity in nlu_entities:
            if (
                entity["entity"] == "verb"
                and entity["confidence"] >= self.ENTITY_CONFIDENCE
            ):
                return ("verb", entity["value"])
        return (None, None)

    def no_intent(self, **kwargs) -> bool:
        """Can't determine the player intent.
        Appends the hint to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.no_intent".format(s=self.state.session.session_id))
        self.output_builder.append(NLG.no_intent())
        self.state.nag_player()
        return True

    def hint(self, **kwargs) -> bool:
        """Use the player AI to get the next possible move.
        Appends the hint to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.hint".format(s=self.state.session.session_id))
        return self.state.get_player().print_next_move()

    def move(
        self, destination: str = None, entity: str = None, nlu_entities: dict = None
    ) -> bool:
        """Attempt to move an entity to a destination determined by NLU or specified.
        Returns whether the move was successful."""
        logger.debug("(SESSION {s}) DM.move".format(s=self.state.session.session_id))
        if not entity:
            entity = "player"
        if not destination and nlu_entities:
            destination = self._get_destination(nlu_entities)[1]

        if not destination:
            moved = False
            self.state.set_expected_entities(["location"])
            connected_rooms = self.state.get_current_room().get_connected_rooms()
            possible_destinations = [
                self.state.get_room_name(room) for room in connected_rooms
            ]
            self.output_builder.append(NLG.no_destination(possible_destinations))
        else:
            logger.debug("(SESSION {s}) Moving {e} to {d}".format(s=self.state.session.session_id, e=entity, d=destination))
            moved = self.actions.move(entity, destination)
        return moved

    def attack(
        self, target: str = None, attacker: str = None, nlu_entities: dict = None
    ) -> bool:
        """Attempt an attack by attacker against target determined by NLU or specified.
        Returns whether the attack was successful."""
        logger.debug("(SESSION {s}) DM.attack".format(s=self.state.session.session_id))
        if not attacker:
            attacker = "player"
        if not target and nlu_entities:
            (target_type, target) = self._get_entity(nlu_entities)
            if not target:
                (target_type, target) = self._get_door(nlu_entities)
            if not target:
                (target_type, target) = self._get_target(nlu_entities)
            (equipment_type, equipment) = self._get_equipment(nlu_entities)
            (item_type, item) = self._get_item(nlu_entities)
            (scenery_type, scenery) = self._get_scenery(nlu_entities)
        else:
            equipment = None
            item = None
            scenery = None
            target_type = None
        
        # check if there's only one possible target
        if target_type == "door" and (not target or target == "door"):
            targets = self.state.get_possible_door_targets()
            if len(targets) == 1:
                target = targets[0]
            else:
                target = None
        elif not target:
            targets = self.state.get_possible_monster_targets()
            if len(targets) == 1:
                target = targets[0].unique_id
                
        if not target:
            attacked = False
            if target_type == "door":
                if not self.state.get_possible_door_targets():
                    self.output_builder.append(NLG.no_door_targets("attack"))
                else:
                    self.state.set_expected_entities(["door", "location"])
                    self.output_builder.append(
                        NLG.no_door_target("attack", self.state.get_formatted_possible_door_targets())
                    )
            else:
                if not self.state.get_possible_monster_targets():
                    self.output_builder.append(NLG.no_monster_targets())
                else:
                    self.state.set_expected_entities(["monster", "npc"])
                    self.output_builder.append(
                        NLG.no_target("attack", self.state.get_formatted_possible_monster_targets())
                    )
        else:
            if target_type == "door":
                logger.debug("(SESSION {s}) {a} is attacking door {t}".format(s=self.state.session.session_id, a=attacker, t=target))
                attacked = self.actions.attack_door(attacker, target)
            else:
                # check if the player tried to use equipment, item or scenery to attack target
                if equipment or item or scenery:
                    if target_type == "monster":
                        self.output_builder.append(NLG.attack_with_non_weapon(self.state.get_entity_name(target), equipment=equipment, item=item, scenery=scenery))
                logger.debug("(SESSION {s}) {a} is attacking {t}".format(s=self.state.session.session_id, a=attacker, t=target))
                attacked = self.actions.attack(attacker, target, target_type=target_type)
        return attacked

    def use(
        self,
        equipment: str = None,
        entity: str = None,
        nlu_entities: dict = None,
        stop: bool = False,
    ) -> bool:
        """Attempt to use an equipment.
        Returns whether the use was successful."""
        logger.debug("(SESSION {s}) DM.use".format(s=self.state.session.session_id))
        if not entity:
            entity = "player"
        if not equipment and nlu_entities:
            equipment = self._get_equipment(nlu_entities)[1]
        
        if not equipment:
            item = self._get_item(nlu_entities)[1]
        if not equipment and not item:
            used = False
            self.output_builder.append(NLG.no_equipment(stop=stop))
        elif equipment:
            logger.debug("(SESSION {s}) {e} is{stop} using: {q}".format(s=self.state.session.session_id, e=entity, q=equipment, stop="stop" if stop else " "))
            used = self.actions.use(equipment=equipment, entity=entity, stop=stop)
        elif item:
            logger.debug("(SESSION {s}) {e} is{stop} using: {q}".format(s=self.state.session.session_id, e=entity, q=item, stop="stop" if stop else " "))
            used = self.actions.use(item=item, entity=entity, stop=stop)
        return used

    def stop_using(
        self, equipment: str = None, entity: str = None, nlu_entities: dict = None
    ) -> bool:
        """Attempt to stop using an equipment.
        Returns whether the stoppage was successful."""
        logger.debug("(SESSION {s}) DM.stop_using".format(s=self.state.session.session_id))
        return self.use(
            equipment=equipment, entity=entity, nlu_entities=nlu_entities, stop=True
        )

    def equip(self, weapon: str = None, entity: str = None, nlu_entities: dict = None):
        """Attempt to equip a weapon.
        Returns whether equipping was successful."""
        logger.debug("(SESSION {s}) DM.equip".format(s=self.state.session.session_id))
        if not entity:
            entity = "player"
        if not weapon and nlu_entities:
            weapon = self._get_weapon(nlu_entities)[1]

        if not weapon:
            equipped = False
            self.output_builder.append(NLG.no_weapon(unequip=False))
        else:
            logger.debug("(SESSION {s}) {e} is equipping {q}".format(s=self.state.session.session_id, e=entity, q=weapon))
            equipped = self.actions.equip(weapon, entity)
        return equipped

    def unequip(
        self, weapon: str = None, entity: str = None, nlu_entities: dict = None
    ) -> bool:
        """Attempt to unequip a weapon.
        Returns whether unequipping was successful."""
        logger.debug("(SESSION {s}) DM.unequip".format(s=self.state.session.session_id))
        if not entity:
            entity = "player"
        if not weapon and nlu_entities:
            weapon = self._get_weapon(nlu_entities)[1]

        if not weapon:
            logger.debug("(SESSION {s}) {e} is unequipping all".format(s=self.state.session.session_id, e=entity))
            unequipped = self.actions.unequip(entity=entity)
        else:
            logger.debug("(SESSION {s}) {e} is unequipping {q}".format(s=self.state.session.session_id, e=entity, q=weapon))
            unequipped = self.actions.unequip(weapon=weapon, entity=entity)
        return unequipped

    def converse(self, target: str = None, nlu_entities: dict = None) -> bool:
        """Attempt to converse with a target determined by NLU or specified.
        Returns whether the action was successful."""
        logger.debug("(SESSION {s}) DM.converse".format(s=self.state.session.session_id))
        if not target and nlu_entities:
            (target_type, target) = self._get_target(nlu_entities)
        elif not target and not nlu_entities:
            target = self._get_npc()[1]

        # check if there's only one possible target
        if not target:
            targets = self.state.get_possible_npc_targets()
            if len(targets) == 1:
                target = targets[0].id
                
        if not target:
            conversation = False
            self.output_builder.append(NLG.no_target("talk to"))
        else:
            logger.debug("(SESSION {s}) Player is conversing with {t}".format(s=self.state.session.session_id, t=target))
            conversation = self.actions.converse(target)
        return conversation

    def affirm(self, **kwargs) -> bool:
        """Player has uttered an affirmation.
        Appends the text to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.affirm".format(s=self.state.session.session_id))
        if not self.state.suggested_next_move["state"] and self.state.received_quest and not self.state.questing:
            logger.debug("(SESSION {s}) Accepted quest".format(s=self.state.session.session_id))
            npc = self.npcs.get_entity(self.state.current_conversation)
            self.output_builder.append(npc.dialogue["accepts_quest"])
            self.state.quest()
        elif self.state.suggested_next_move["state"]:
            logger.debug("(SESSION {s}) Accepted suggested next move: {n}".format(s=self.state.session.session_id, n=self.state.suggested_next_move["utter"]))
            utter = self.state.suggested_next_move["utter"]
            (intent, params) = self.nlu.process_player_utterance(utter)
            return self.input(utter, intent=intent, kwargs=params)
        elif "roll" in self.state.expected_intent:
            return self.roll()
        return True

    def deny(self, **kwargs) -> bool:
        """Player has uttered a denial.
        Appends the text to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.deny".format(s=self.state.session.session_id))
        if self.state.roleplaying and self.state.received_quest and not self.state.questing:
            # this is a game end condition
            npc = self.npcs.get_entity(self.state.current_conversation)
            self.output_builder.append(npc.dialogue["turns_down_quest"])
            self.output_builder.append(self.get_bad_ending())
            self.state.gameover()
        return True

    def explore(self, target: str = None, target_type: str = None, nlu_entities: dict = None) -> bool:
        """Attempt to explore/investigate.
        Returns whether the action was successful."""
        logger.debug("(SESSION {s}) DM.explore".format(s=self.state.session.session_id))
        if not target and nlu_entities:
            (target_type, target) = self._get_noun(nlu_entities)
        # TODO if not target, get any noun (not just those in NLU entitities) as targets
        
        # check if there's only one possible door target - if so, use it
        if target_type == "door" and target == "door":
            if len(self.state.get_current_room().get_connected_rooms()) == 1:
                target = self.state.get_current_room().get_connected_rooms()[0]
            else:
                targets = self.state.get_possible_door_targets()
                if len(targets) == 1:
                    target = targets[0]
                
        if not target or (target_type == "location" and self.state.get_current_room_id() == target):
            logger.debug("(SESSION {s}) Player is exploring".format(s=self.state.session.session_id))
            room = self.state.get_current_room()
            self.output_builder.append(room.get_description())
            # trigger the explore triggers in the room
            room.explore_trigger()
            explore = True
        else:
            logger.debug("(SESSION {s}) Player is investigating {t}".format(s=self.state.session.session_id, t=target))
            explore = self.actions.investigate(target, target_type=target_type)
        if explore:
            self.state.explore()
        return explore

    def roll(
        self, entity: str = "player", die: str = None, nlu_entities: dict = {}
    ) -> bool:
        """Attempt to roll die.
        Returns whether the action was successful."""
        logger.debug("(SESSION {s}) DM.roll".format(s=self.state.session.session_id))

        # If there's a stored intent, ignore the player specified die and use correct one
        if self.state.stored_intent:
            if "nlu_entities" in self.state.stored_intent["params"]:
                nlu_entities.extend(self.state.stored_intent["params"]["nlu_entities"])
            if self.state.stored_intent["intent"] == "attack":
                if self.state.in_combat_with_door:
                    return self.actions.roll("door_attack")
                else:
                    return self.actions.roll("attack")
            elif self.state.stored_intent["intent"] == "force":
                if self.state.stored_ability_check:
                    return self.actions.roll("ability_check")
            
        if self.state.in_combat_with_door:
            return self.actions.roll("door_attack")
        if self.state.in_combat:
            return self.actions.roll("attack")
        if self.state.stored_ability_check:
            return self.actions.roll("ability_check")
        if self.state.stored_skill_check:
            return self.actions.roll("skill_check")

        # not stored intent, get the dice spec now
        if not die and nlu_entities:
            die = self._get_die(nlu_entities)[1]
        return self.actions.roll("roll", nlu_entities, die)

    def pick_up(self, entity: str = "player", item: str = None, nlu_entities: dict = {}) -> bool:
        """Attempt to pick up an item.
        Returns whether the action was successful."""
        logger.debug("(SESSION {s}) DM.pick_up".format(s=self.state.session.session_id))
        if not entity:
            entity = "player"
        if not item and nlu_entities:
            item = self._get_item(nlu_entities)[1]

        if not item:
            # check if item is puzzle item
            (item_type, item) = self._get_target(nlu_entities)
            if item and item_type == "puzzle":
                # trigger explore
                picked_up = self.actions.investigate(item, target_type=item_type)
        if not item:
            picked_up = False
            self.output_builder.append(NLG.no_item())
        else:
            logger.debug("(SESSION {s}) {e} is picking up {i}".format(s=self.state.session.session_id, e=entity, i=item))
            picked_up = self.actions.pick_up(item, entity)
        return picked_up

    def health(self, **kwargs) -> bool:
        """Player wants a health update.
        Appends the text to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.health".format(s=self.state.session.session_id))
        player = self.state.get_player()
        hp = self.state.get_current_hp()
        self.output_builder.append(NLG.health_update(hp, hp_max=player.hp_max))
        return True

    def inventory(self, **kwargs) -> bool:
        """Player wants a inventory update.
        Appends the text to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.inventory".format(s=self.state.session.session_id))
        item_collection = self.state.get_player().character.items
        self.output_builder.append(item_collection.get_all_formatted())
        return True

    def force(self, target: str = None, entity: str = None, nlu_entities: dict = {}) -> bool:
        """Player wants to attempt to force a target.
        Appends the text to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.force".format(s=self.state.session.session_id))
        if not entity:
            entity = "player"
        if not target and nlu_entities:
            (target_type, target) = self._get_target(nlu_entities)
        else:
            target_type = None
        
        if target and (target_type != "door" and target_type != "puzzle"):
            forced = False
            self.output_builder.append(NLG.not_force_target(target))
            return forced
        
        # check if there's only one possible target
        if target_type == "door" and (not target or target == "door"):
            targets = self.state.get_possible_door_targets()
            if len(targets) == 1:
                target = targets[0]
            elif len(self.state.get_current_room().get_connected_rooms()) == 1:
                target = self.state.get_current_room().get_connected_rooms()[0]
        
        # TODO add additional code for puzzle target
            
        if not target:
            forced = False
            if not self.state.get_possible_door_targets():
                self.output_builder.append(NLG.no_door_targets("force"))
            else:
                self.state.set_expected_entities(["door", "location"])
                self.output_builder.append(
                    NLG.no_door_target("force", self.state.get_formatted_possible_door_targets())
                )
        else:
            logger.debug("(SESSION {s}) {e} is forcing door {t}".format(s=self.state.session.session_id, e=entity, t=target))
            forced = self.actions.ability_check("str", entity, target, target_type)
        return forced

    def ability_check(self, **kwargs) -> bool:
        """Player wants to attempt to perform a ability check.
        Appends the text to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.ability_check".format(s=self.state.session.session_id))
        if self.state.stored_ability_check or "ability_check" in self.state.stored_intent:
            logger.debug("(SESSION {s}) Player is performing ability check".format(s=self.state.session.session_id))
            return self.roll(**kwargs)
        else:
            self.output_builder.append("You can do an ability check when I ask you to.")
            return True
        
    def skill_check(self, **kwargs) -> bool:
        """Player wants to attempt to perform a skill check.
        Appends the text to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.skill_check".format(s=self.state.session.session_id))
        if self.state.stored_skill_check or "skill_check" in self.state.stored_intent:
            logger.debug("(SESSION {s}) Player is performing skill check".format(s=self.state.session.session_id))
            return self.roll(**kwargs)
        else:
            self.output_builder.append("You can do a skill check when I ask you to.")
            return True

    def ale(self, nlu_entities: dict = {}) -> bool:
        """Player wants to attempt to drink some ale.
        Appends the text to output with the self.output_builder.
        """
        logger.debug("(SESSION {s}) DM.ale".format(s=self.state.session.session_id))
        if nlu_entities:
            drink = self._get_drink(nlu_entities)[1]
            if drink != "ale":
                self.output_builder.append("They only serve ale here!")
        if self.state.get_current_room().ale:
            logger.debug("(SESSION {s}) Player is getting an ale".format(s=self.state.session.session_id))
            if self.state.ales > 2:
                # this is a gameover state
                self.output_builder.append(NLG.drunk_end_game())
                self.output_builder.append(self.get_bad_ending())
                self.state.gameover()
                return
            self.output_builder.append(NLG.drink_ale(self.state.ales))
            self.state.drink_ale()
        else:
            self.output_builder.append("You wish you could get an ale here!")
            
    def roleplay(self, nlu_entities: dict = None) -> bool:
        """Attempt to roleplay.
        Returns whether the action was successful."""
        logger.debug("(SESSION {s}) DM.roleplay".format(s=self.state.session.session_id))
        verb = None
        target = None
        target_type = None
        if nlu_entities:
            (verb_type, verb) = self._get_verb(nlu_entities)
            (target_type, target) = self._get_noun(nlu_entities)

        if not verb:
            roleplay = False
            self.output_builder.append(NLG.no_roleplay(target))
            self.state.nag_player()
        else:
            logger.debug("(SESSION {s}) Player is roleplaying \"{v}\" with {t}".format(s=self.state.session.session_id, v=verb, t=str(target)))
            roleplay = self.actions.roleplay(verb, target, self._player_utter, target_type)
        return roleplay
    
    def negotiate(self, **kwargs) -> bool:
        """Attempt to negotiate.
        Returns whether the action was successful."""
        logger.debug("(SESSION {s}) DM.negotiate".format(s=self.state.session.session_id))
        (npc_type, npc) = self._get_npc()
        if npc and self.state.get_entity(npc).gives_quest:
            logger.debug("(SESSION {s}) Player is negotiating with {n}".format(s=self.state.session.session_id, n=npc))
            if self.state.get_entity(npc).dialogue:
                self.state.roleplay(npc)
                self.state.set_conversation_target(npc)
            self.output_builder.append(self.state.get_entity(npc).dialogue["no_negotiation"])
            if not self.state.questing:
                self.output_builder.append(self.state.get_entity(npc).dialogue["quest_prompt"])
        else:
            self.output_builder.append("There's nobody to negotiate with here.")
            self.state.nag_player()
        return True
    
    def rescue(self, **kwargs) -> bool:
        """Attempt to rescue.
        Returns whether the action was successful."""
        logger.debug("(SESSION {s}) DM.rescue".format(s=self.state.session.session_id))
        (npc_type, npc) = self._get_npc()
        if "rescue" in self.state.get_entity(npc).dialogue:
            logger.debug("(SESSION {s}) Player is rescuing {n}".format(s=self.state.session.session_id, n=npc))
            self.output_builder.append(self.state.get_entity(npc).dialogue["rescue"])
        else:
            self.output_builder.append("There's nobody to rescue here")
            self.state.nag_player()
        return True
    
    def bot_challenge(self, **kwargs) -> bool:
        """Describe self to player."""
        logger.debug("(SESSION {s}) DM.bot_challenge".format(s=self.state.session.session_id))
        self.output_builder.append("I'm an AI made by Katie Baker, I'm designed to play RPGs with you!")
        return True

    def stealth(self, **kwargs) -> bool:
        """Describe self to player."""
        logger.debug("(SESSION {s}) DM.stealth".format(s=self.state.session.session_id))
        self.output_builder.append("Unfortunately, being stealthy doesn't do anything in this game... except to make you look cool and mysterious.")
        self.state.nag_player()
        return True

    def pick_lock(self, **kwargs) -> bool:
        """Describe self to player."""
        logger.debug("(SESSION {s}) DM.pick_lock".format(s=self.state.session.session_id))
        item_collection = self.state.get_player().character.items
        if not item_collection.has_item("thieves_tools")[0]:
            self.output_builder.append("Unfortunately, you don't have the required tools in order to pick locks.")
            self.state.nag_player()
        return True