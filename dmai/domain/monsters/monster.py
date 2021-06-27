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
from dmai.utils.output_builder import OutputBuilder
from dmai.utils.dice_roller import DiceRoller
from dmai.utils.text import Text
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Monster(NPC, MonsterAgent):
    def __init__(
        self,
        monster_data: dict,
        npc_data: dict = None,
        unique_id: str = None,
        unique_name: str = None,
    ) -> None:
        """Monster abstract class"""
        if unique_id:
            MonsterAgent.__init__(self, problem=unique_id)
        else:
            MonsterAgent.__init__(self, problem=monster_data["id"])
        if npc_data:
            NPC.__init__(self, npc_data)

        try:
            for key in monster_data:
                self.__setattr__(key, monster_data[key])

            # replace the attributes values with objects where appropriate
            self.abilities = Abilities(self.abilities)
            self.alignment = Alignment(self.alignment)
            self.armor = Armor(self.armor)
            self.attacks = Attacks(self.attacks)
            self.conditions = Conditions()
            self.equipment = EquipmentCollection(self.equipment)
            self.features = Features(features=self.features)
            self.languages = Languages(self.languages)
            self.skills = Skills(abilities=self.abilities, skills=self.skills)
            self.spells = Spells(self.spells)

        except AttributeError as e:
            logger.error("Cannot create monster, incorrect attribute: {e}".format(e=e))
            raise

        # Initialise additional variables
        self.unique_id = unique_id
        self.treasure = None
        self.must_kill = False
        self.will_attack_player = False

        # set unique name
        self.unique_name = unique_name
        if not self.unique_name:
            i = self.unique_id.split("_")[-1]
            self.unique_name = "{n} {i}".format(n=self.name, i=i)

        # set up triggers
        self.trigger_map = {
            "attack_of_opportunity": {
                "can_trigger": True,
                "trigger": self.attack_of_opportunity,
            }
        }

        # character-specific triggers must be determined from the adventure
        if npc_data:
            if npc_data["triggers"]:
                if "move" in npc_data["triggers"]:
                    self.trigger_map["move"] = {
                        "can_trigger": True,
                        "trigger": self.move,
                        "params": {
                            "destination": npc_data["triggers"]["move"],
                            "conditions": npc_data["triggers"]["conditions"],
                        },
                    }

    def __repr__(self) -> str:
        return "Monster: {n}\nMax HP: {hp}".format(n=self.name, hp=self.hp_max)

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
        return DiceRoller.roll(die, silent=True)

    def attack_roll(self, weapon: str) -> int:
        """Method to roll attack"""
        die = "d20{m}".format(m=self.get_signed_attack_bonus(weapon))
        return DiceRoller.roll(die, silent=True)

    def damage_roll(self, weapon: str) -> int:
        """Method to roll damage"""
        dice_spec = self.get_damage_dice(weapon)
        return DiceRoller.roll_dice(dice_spec, silent=True)

    def set_treasure(self, treasure: str) -> None:
        """Method to set treasure."""
        self.treasure = treasure

    def set_must_kill(self, must_kill: bool) -> None:
        """Method to set must_kill."""
        self.must_kill = must_kill

    def set_will_attack_player(self, will_attack_player: bool) -> None:
        """Method to set will_attack_player."""
        self.will_attack_player = will_attack_player

    def get_all_attack_ids(self) -> list:
        """Method to get all attack IDs of monster"""
        return self.attacks.get_all_attack_ids()

    # =============================================
    # TRIGGERS
    def attack_of_opportunity(self) -> None:
        """Method to perform an attack of opportunity"""
        logger.debug(
            "Triggering attack of opportunity in monster: {m}".format(m=self.id)
        )
        if not State.stationary and State.in_combat and State.is_alive(self.id):
            OutputBuilder.append(NLG.attack_of_opportunity(attacker=self.name))

    def move(self, destination: str, conditions: dict) -> None:
        """Method to move as a reaction to some situation"""
        logger.debug("Triggering movement of monster: {m}".format(m=self.id))
        if State.is_alive(self.id):
            if "monsters" in conditions:
                if conditions["monsters"] == "dead":
                    location = State.get_current_room_id(self.unique_id)
                    if not State.get_dm().npcs.get_monster_id(monster_type="giant_rat", status="alive", location=location):
                        State.set_current_room(self.unique_id, destination)

    def trigger(self) -> None:
        """Method to perform any actions or print any new text if conditions met"""
        for trigger_type in self.trigger_map:
            if self.trigger_map[trigger_type]["can_trigger"]:
                if "params" in self.trigger_map[trigger_type]:
                    self.trigger_map[trigger_type]["trigger"](
                        **self.trigger_map[trigger_type]["params"]
                    )
                else:
                    self.trigger_map[trigger_type]["trigger"]()
