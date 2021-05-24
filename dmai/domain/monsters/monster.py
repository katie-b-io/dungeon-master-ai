from dmai.game.npcs.npc import NPC
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
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Monster(NPC):
    def __init__(self, monster_data: dict, npc_data: dict = None) -> None:
        """Monster abstract class"""
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
        self.treasure = None
        
        self.trigger_map = {
            "attack_of_opportunity": {
                "can_trigger": True,
                "trigger": self.attack_of_opportunity
            }
        }

    def __repr__(self) -> str:
        return "Monster: {n}\nMax HP: {hp}".format(n=self.name, hp=self.hp_max)

    def set_treasure(self, treasure: str) -> None:
        """Method to set treasure."""
        self.treasure = treasure

    def attack_of_opportunity(self) -> None:
        """Method to perform an attack of opportunity"""
        logger.debug("Triggering attack of opportunity in monster: {m}".format(m=self.id))
        if not State.stationary:
            OutputBuilder.append(NLG.attack_of_opportunity(attacker=self.name))
        
    def trigger(self) -> None:
        """Method to perform any actions or print any new text if conditions met"""
        for trigger_type in self.trigger_map:
            if self.trigger_map[trigger_type]["can_trigger"]:
                self.trigger_map[trigger_type]["trigger"]()