from dmai.utils.output_builder import OutputBuilder
from dmai.game.npcs.npc import NPC
from dmai.agents.monster_agent import MonsterAgent
from dmai.domain.abilities import Abilities
from dmai.domain.alignment import Alignment
from dmai.domain.armor import Armor
from dmai.domain.attacks import Attacks
from dmai.domain.conditions import Conditions
from dmai.domain.equipment.equipment_collection import EquipmentCollection
from dmai.domain.features import Features
from dmai.domain.languages import Languages
from dmai.domain.skills import Skills
from dmai.domain.spells import Spells
from dmai.game.state import State
from dmai.nlg.nlg import NLG
from dmai.utils.dice_roller import DiceRoller
from dmai.utils.text import Text
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Monster(NPC, MonsterAgent):
    def __init__(
        self,
        monster_data: dict,
        state: State,
        output_builder: OutputBuilder,
        npc_data: dict = None,
        unique_id: str = None,
        unique_name: str = None,
    ) -> None:
        """Monster abstract class"""
        if unique_id:
            MonsterAgent.__init__(self, state, output_builder, problem=unique_id)
        else:
            MonsterAgent.__init__(self, state, output_builder, problem=monster_data["id"])
        if npc_data:
            NPC.__init__(self, state, npc_data)

        try:
            for key in monster_data:
                self.__setattr__(key, monster_data[key])

            # replace the attributes values with objects where appropriate
            self.abilities = Abilities(self.abilities)
            self.alignment = Alignment(self.state, self.alignment)
            self.armor = Armor(self.armor)
            self.attacks = Attacks(self.attacks)
            self.conditions = Conditions()
            self.equipment = EquipmentCollection(self.equipment, self.state, self.output_builder)
            self.features = Features(features=self.features)
            self.languages = Languages(self.languages)
            self.skills = Skills(abilities=self.abilities, skills=self.skills)
            self.spells = Spells(self.spells)

        except AttributeError as e:
            logger.error("(SESSION {s}) Cannot create monster, incorrect attribute: {e}".format(s=self.state.session.session_id, e=e))
            raise

        # Initialise additional variables
        self.unique_id = unique_id
        self.must_kill = False
        self.attack_player_after_n_moves = -1
        self.will_attack_player = False

        # set unique name
        self.unique_name = unique_name
        if not self.unique_name:
            i = self.unique_id.split("_")[-1]
            self.unique_name = "{n} {i}".format(n=self.name, i=i)

        # set up triggers
        if self.unique_id not in self.state.monster_trigger_map:
            self.state.monster_trigger_map[unique_id] = {}
        
        if self.unique_id not in self.state.monster_turn_counter:
            self.state.monster_turn_counter[unique_id] = 0

        if "attack_of_opportunity" not in self.state.monster_trigger_map[unique_id]:
            self.state.monster_trigger_map[unique_id]["attack_of_opportunity"] = True

        if "attack" not in self.state.monster_trigger_map[unique_id]:
            self.state.monster_trigger_map[unique_id]["attack"] = True

        if "increment" not in self.state.monster_trigger_map[unique_id]:
            self.state.monster_trigger_map[unique_id]["increment"] = True

        self.trigger_map = {
            "attack_of_opportunity": {
                "trigger": self.attack_of_opportunity,
            },
            "attack": {
                "trigger": self.attack
            },
            "increment": {
                "trigger": self.increment
            }
        }

        # character-specific triggers must be determined from the adventure
        if npc_data:
            if npc_data["triggers"]:
                if "move" in npc_data["triggers"]:
                    if "move" not in self.state.monster_trigger_map[self.unique_id]:
                        self.state.monster_trigger_map[self.unique_id]["move"] = True
                    self.trigger_map["move"] = {
                        "trigger": self.move,
                        "params": {
                            "destination": npc_data["triggers"]["move"]["destination"],
                            "conditions": npc_data["triggers"]["move"]["conditions"],
                        },
                    }

    def __repr__(self) -> str:
        return "Monster: {n}".format(n=self.unique_id)

    @property
    def initiative(self) -> int:
        """Method to return the initiative attribute"""
        return self.abilities.get_modifier("dex")

    @property
    def armor_class(self) -> int:
        """Method to return the armor class"""
        return self.ac
    
    def has_darkvision(self) -> bool:
        """Method to return whether monster has darkvision"""
        return "darkvision" in self.senses

    def get_signed_initiative(self) -> str:
        """Method to return the signed initiative"""
        return Text.get_signed_value(self.initiative)

    def get_signed_attack_bonus(self, attack_id: str) -> str:
        """Method to return the signed attack bonus"""
        attack = self.attacks.get_attack(attack_id)
        return Text.get_signed_value(attack["attack_bonus"])

    def get_damage_dice(self, attack_id: str) -> dict:
        """Method to return the damage dice spec"""
        attack = self.attacks.get_attack(attack_id)
        return attack["hit"]["damage"]

    def initiative_roll(self) -> int:
        """Method to roll initiative"""
        die = "d20{m}".format(m=self.get_signed_initiative())
        (roll_str, roll) = DiceRoller.roll(die, silent=True)
        return roll

    def attack_roll(self, weapon: str) -> int:
        """Method to roll attack"""
        die = "d20{m}".format(m=self.get_signed_attack_bonus(weapon))
        (roll_str, roll) = DiceRoller.roll(die, silent=True)
        return roll

    def damage_roll(self, weapon: str) -> int:
        """Method to roll damage"""
        dice_spec = self.get_damage_dice(weapon)
        (roll_str, roll) = DiceRoller.roll_dice(dice_spec, silent=True)
        if roll < 0:
            roll = 0
        self.output_builder.append(roll_str)
        return roll

    def min_damage(self, weapon: str) -> int:
        """Method to return minimum possible damage"""
        dice_spec = self.get_damage_dice(weapon)
        (roll_str, roll) = DiceRoller.get_min(dice_spec=dice_spec)
        if roll < 0:
            roll = 0
        self.output_builder.append(roll_str)
        return roll

    def set_treasure(self, treasure: list) -> None:
        """Method to set treasure."""
        if self.unique_id not in self.state.monster_treasure_map:
            self.state.monster_treasure_map[self.unique_id] = treasure

    def set_must_kill(self, must_kill: bool) -> None:
        """Method to set must_kill."""
        self.must_kill = must_kill

    def set_attack_player_after_n_moves(self, attack_player_after_n_moves: int) -> None:
        """Method to set attack_player_after_n_moves."""
        self.attack_player_after_n_moves = attack_player_after_n_moves
        self.will_attack_player = attack_player_after_n_moves == 0

    def get_all_attack_ids(self) -> list:
        """Method to get all attack IDs of monster"""
        return self.attacks.get_all_attack_ids()

    def took_item(self, item: str) -> None:
        """Method to remove the item from the monster treasure"""
        self.state.monster_treasure_map[self.unique_id].remove(item)
        
    # =============================================
    # TRIGGERS
    def attack_of_opportunity(self) -> None:
        """Method to perform an attack of opportunity"""
        if not self.state.stationary and self.state.in_combat and self.state.is_alive(self.unique_id):
            logger.debug("(SESSION {s}) Triggering attack of opportunity in monster: {m}".format(s=self.state.session.session_id, m=self.unique_id))
            self.output_builder.append(NLG.attack_of_opportunity(attacker=self.name))

    def move(self, destination: str, conditions: dict) -> None:
        """Method to move as a reaction to some situation"""
        if self.state.is_alive(self.unique_id):
            if "monsters" in conditions:
                if conditions["monsters"] == "dead":
                    location = self.state.get_current_room_id(self.unique_id)
                    if not self.state.get_dm().npcs.get_monster_id(monster_type="giant_rat", status="alive", location=location):
                        logger.debug("(SESSION {s}) Triggering movement of monster: {m}".format(s=self.state.session.session_id, m=self.unique_id))
                        self.state.set_current_room(self.unique_id, destination)

    def attack(self) -> None:
        """Method to attack player"""
        if self.state.is_alive(self.unique_id):
            if not self.state.expected_intent:
                if self.will_attack_player:
                    location = self.state.get_current_room(self.unique_id)
                    if location == self.state.get_current_room():
                        if not self.state.in_combat:
                            logger.debug("(SESSION {s}) Triggering combat with player: {m}".format(s=self.state.session.session_id, m=self.unique_id))
                            if "monster_attack" in location.text:
                                self.output_builder.append(location.text["monster_attack"]["text"])
                            self.state.combat(self.unique_id, "player")
    
    def increment(self) -> None:
        """Method to increment number of turns player and monster in same room"""
        if self.state.is_alive(self.unique_id):
            location = self.state.get_current_room_id(self.unique_id)
            if location == self.state.get_current_room_id():
                self.state.monster_turn_counter[self.unique_id] += 1
                if not self.will_attack_player and (self.state.monster_turn_counter[self.unique_id] == self.attack_player_after_n_moves):
                    self.will_attack_player = True

    def trigger(self) -> None:
        """Method to perform any actions or print any new text if conditions met"""
        for trigger_type in self.trigger_map:
            if self.state.monster_trigger_map[self.unique_id][trigger_type]:
                if "params" in self.trigger_map[trigger_type]:
                    self.trigger_map[trigger_type]["trigger"](
                        **self.trigger_map[trigger_type]["params"]
                    )
                else:
                    self.trigger_map[trigger_type]["trigger"]()
