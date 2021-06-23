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
    def __init__(self, monster_data: dict, npc_data: dict = None, unique_id: str = None, unique_name: str = None) -> None:
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
            logger.error(
                "Cannot create monster, incorrect attribute: {e}".format(e=e))
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
            self.unique_name = "{n} {i}".format(n=self.name, i={i})

        self.trigger_map = {
            "attack_of_opportunity": {
                "can_trigger": True,
                "trigger": self.attack_of_opportunity
            }
        }

    def __repr__(self) -> str:
        return "Monster: {n}\nMax HP: {hp}".format(n=self.name, hp=self.hp_max)

    @property
    def initiative(self) -> int:
        """Method to return the initiative attribute"""
        return self.abilities.get_modifier("dex")

    def get_signed_initiative(self) -> str:
        """Method to return the signed initiative"""
        return Text.get_signed_value(self.initiative)
    
    def roll_initiative(self) -> int:
        """Method to roll initiative"""
        die = "d20{m}".format(m=self.get_signed_initiative())
        return DiceRoller.roll(die, silent=True)
    
    def set_treasure(self, treasure: str) -> None:
        """Method to set treasure."""
        self.treasure = treasure

    def set_must_kill(self, must_kill: bool) -> None:
        """Method to set must_kill."""
        self.must_kill = must_kill

    def set_will_attack_player(self, will_attack_player: bool) -> None:
        """Method to set will_attack_player."""
        self.will_attack_player = will_attack_player
        
    def attack_of_opportunity(self) -> None:
        """Method to perform an attack of opportunity"""
        logger.debug("Triggering attack of opportunity in monster: {m}".format(
            m=self.id))
        if not State.stationary:
            OutputBuilder.append(NLG.attack_of_opportunity(attacker=self.name))

    def trigger(self) -> None:
        """Method to perform any actions or print any new text if conditions met"""
        for trigger_type in self.trigger_map:
            if self.trigger_map[trigger_type]["can_trigger"]:
                self.trigger_map[trigger_type]["trigger"]()
    
    def get_all_attack_ids(self) -> list:
        """Method to get all attack IDs of monster"""
        return self.attacks.get_all_attack_ids()
    