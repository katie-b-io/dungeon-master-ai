from abc import ABC
import textwrap

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
from dmai.domain.weapons import Weapons
from dmai.domain.characters.character_class import CharacterClass
from dmai.domain.characters.race import Race
from dmai.utils.dice_roller import DiceRoller
from dmai.utils.text import Text
from dmai.utils.money import Money
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Character(ABC):
    def __init__(self, character_data: dict) -> None:
        """Character abstract class"""
        self.name = None
        self.cp = 0

        try:
            for key in character_data:
                self.__setattr__(key, character_data[key])

            # replace the attributes values with objects where appropriate
            self.abilities = Abilities(self.abilities)
            self.alignment = Alignment(self.alignment)
            self.attacks = Attacks()
            self.char_class = CharacterClass(self.char_class)
            self.conditions = Conditions()
            self.equipment = EquipmentCollection(
                equipment=self.equipment,
                proficiencies=self.proficiencies["tools"])
            self.languages = Languages(self.languages)
            self.race = Race(self.race)
            self.skills = Skills(
                abilities=self.abilities,
                pro_bonus=self.proficiency_bonus,
                proficiencies=self.proficiencies["skills"],
            )
            self.spells = Spells(self.spells)
            self.weapons = Weapons(
                self.weapons, proficiencies=self.get_proficiencies("weapons"))
            self.armor = Armor(self.armor,
                               proficiencies=self.get_proficiencies("armor"))
            self.features = Features(char_class=self.char_class,
                                     race=self.race)

        except AttributeError as e:
            logger.error(
                "Cannot create character, incorrect attribute: {e}".format(
                    e=e))
            raise

    def __repr__(self) -> str:
        return "Character: {n}".format(n=self.name)

    @property
    def hp_max(self) -> int:
        """Method to return the maximum hit points"""
        hp = DiceRoller.get_max(self.char_class.hit_dice)
        mod = self.abilities.get_modifier("con")
        return hp + mod

    @property
    def initiative(self) -> int:
        """Method to return the initiative attribute"""
        return self.get_ability_modifier("dex")

    @property
    def speed(self) -> int:
        """Method to return the speed attribute"""
        return self.race.speed

    @property
    def passive_wisdom(self) -> int:
        """Method to return the passive wisdom attribute"""
        return 10 + self.abilities.get_modifier("wis")

    @property
    def armor_class(self) -> int:
        """Method to return the armor class (AC) attribute"""
        return self.armor.calculate_armor_class(
            self.get_ability_modifier("dex"))

    def has_darkvision(self) -> bool:
        """Method to return bool for whether character has darkvision"""
        return self.features.contains(
            "darkvision_elf") or self.features.contains("darkvision_dwarf")

    def has_equipment(self, equipment: str) -> tuple:
        """Method to check whether player has specified equipment"""
        return self.equipment.has_equipment(equipment)

    def use_equipment(self, equipment: str) -> bool:
        """Method to use specified equipment"""
        return self.equipment.use_equipment(equipment)

    def stop_using_equipment(self, equipment: str) -> bool:
        """Method to stop using specified equipment"""
        return self.equipment.stop_using_equipment(equipment)

    def can_equip(self, weapon: str) -> tuple:
        """Method to check whether player can equip specified weapon"""
        return self.weapons.can_equip(weapon)

    def can_unequip(self, weapon: str) -> tuple:
        """Method to check whether player can unequip specified weapon"""
        return self.weapons.can_unequip(weapon)

    def is_equipped(self, weapon: str) -> bool:
        """Method to check whether weapon is equipped"""
        return self.weapons.is_equipped(weapon)

    def equip_weapon(self, weapon: str) -> bool:
        """Method to equip specified weapon"""
        return self.weapons.equip_weapon(weapon)

    def unequip_weapon(self, weapon: str = None) -> bool:
        """Method to unequip specified weapon"""
        return self.weapons.unequip_weapon(weapon)

    def get_proficiencies(self, prof_type: str) -> list:
        """Method to return list of proficiencies of specified type"""
        all_prof = []
        if prof_type != "skills":
            if self.char_class.get_proficiencies(prof_type):
                all_prof.extend(self.char_class.get_proficiencies(prof_type))
        if prof_type in self.proficiencies:
            for prof_reason in self.proficiencies[prof_type]:
                all_prof.extend(self.proficiencies[prof_type][prof_reason])
        return all_prof

    def get_class(self) -> str:
        """Method to return character class in string"""
        return self.char_class.get_formatted_class()

    def get_race(self) -> str:
        """Method to return character race in string"""
        return self.race.name

    def get_alignment(self) -> str:
        """Method to return character race in string"""
        return self.alignment.name

    def get_ability_score(self, ability: str) -> int:
        """Method to return the specified ability score"""
        return self.abilities.get_score(ability)

    def get_ability_modifier(self, ability: str) -> int:
        """Method to return the specified ability modifier"""
        return self.abilities.get_modifier(ability)

    def get_skill_modifier(self, skill: str) -> int:
        """Method to return the specified skill modifier"""
        return self.skills.get_modifier(skill)

    def get_signed_ability_modifier(self, ability: str) -> str:
        """Method to return the signed ability modifier"""
        return Text.get_signed_value(self.get_ability_modifier(ability))

    def get_signed_saving_throw(self, ability: str) -> str:
        """Method to return the signed saving throw"""
        return Text.get_signed_value(self.get_saving_throw(ability))

    def get_signed_skill_modifier(self, skill: str) -> str:
        """Method to return the skill signed modifier"""
        return Text.get_signed_value(self.get_skill_modifier(skill))

    def get_signed_initiative(self) -> str:
        """Method to return the signed initiative"""
        return Text.get_signed_value(self.initiative)

    def get_signed_attack_bonus(self, weapon_id: str) -> str:
        """Method to return the signed attack bonus"""
        if self.weapons.has_property(
                weapon_id, "finesse") or self.weapons.is_ranged(weapon_id):
            m = self.get_ability_modifier("dex")
        else:
            m = self.get_ability_modifier("str")
        return Text.get_signed_value(m + self.proficiency_bonus)

    def get_saving_throw(self, ability: str) -> int:
        """Method to return the specified saving throw"""
        if ability in self.char_class.proficiencies["saving_throws"]:
            return self.proficiency_bonus + self.get_ability_modifier(ability)
        else:
            return self.get_ability_modifier(ability)

    def get_formatted_ability(self, ability: str) -> str:
        """Method to return the specified ability string"""
        m = self.get_signed_ability_modifier(ability)
        return "{m} ({a})".format(m=m, a=self.get_ability_score(ability))

    def get_formatted_saving_throw(self, ability: str) -> str:
        """Method to return the specified saving throw formatted string"""
        s = self.get_signed_saving_throw(ability)
        if ability in self.char_class.proficiencies["saving_throws"]:
            return "{s} (proficiency)".format(s=s)
        else:
            return "{s}".format(s=s)

    def get_formatted_skill_modifier(self, skill: str) -> str:
        """Method to return the specified skill modifier formatted string"""
        m = self.get_signed_skill_modifier(skill)
        if ("expertise" in self.proficiencies["skills"]
                and skill in self.proficiencies["skills"]["expertise"]):
            return "{m} (expertise)".format(m=m)
        elif skill in self.proficiencies["skills"]["class"]:
            return "{m} (proficiency)".format(m=m)
        else:
            return "{m}".format(m=m)

    def get_formatted_speed(self) -> str:
        """Method to return the speed formatted string"""
        return "{s} ft".format(s=self.speed)

    def get_all_weapons(self) -> list:
        """Method to return a list of character's weapons in tuple (id, name)"""
        return [(weapon["id"], weapon["name"])
                for weapon in self.weapons.get_all()]

    def get_formatted_attack(self, weapon_id: str) -> str:
        """Method to return the attack formatted string"""
        d = self.weapons.get_damage(weapon_id)
        if self.weapons.has_property(
                weapon_id, "finesse") or self.weapons.is_ranged(weapon_id):
            m = self.get_signed_ability_modifier("dex")
        else:
            m = self.get_signed_ability_modifier("str")
        t = self.weapons.get_damage_type(weapon_id)

        if m == " 0":
            return "{d} ({t})".format(d=d, t=t)
        else:
            return "{d} {m} ({t})".format(d=d, m=m, t=t)

    def get_formatted_armor(self) -> str:
        """Method to return the armor formatted string"""
        armor_str = ", ".join([
            self.armor.get_formatted(e) for e in self.armor.get_all()
        ])
        return "\n".join(textwrap.wrap(armor_str, 75))

    def get_formatted_equipment(self) -> str:
        """Method to return the equipment formatted string"""
        equipment_str = ", ".join([
            self.equipment.get_formatted(e) for e in self.equipment.get_all()
        ])
        return "\n".join(textwrap.wrap(equipment_str, 75))

    def get_formatted_money(self) -> str:
        """Method to return the money formatted string"""
        return Money.get_formatted(self.cp)

    def get_formatted_languages(self) -> str:
        """Method to return the languages formatted string"""
        return Text.properly_format_list(
            [language["name"] for language in self.languages.get_all()])

    def get_all_features(self) -> list:
        """Method to return a list of character's features in tuple (id, name)"""
        return [(feature["id"], feature["name"])
                for feature in self.features.get_all()]

    def get_feature_description(self,
                                feature_id: str,
                                indent_length: int = 20) -> str:
        """Method to return the feature description string"""
        desc = self.features.get_description(feature_id)
        empty_str = " " * indent_length
        wrapped = textwrap.wrap(desc, 75)
        # append the indentation to second line onwards
        for w_str in wrapped:
            i = wrapped.index(w_str)
            if i > 0:
                wrapped[i] = empty_str + w_str
        return "\n".join(wrapped)

    def get_formatted_proficiencies(self):
        """Method to return a list of character's proficiencies in tuple (proficiency_type, [id])"""
        prof_list = []

        prof_armor = [a["name"] for a in self.armor.get_proficient()]
        prof_weapons = [w["name"] for w in self.weapons.get_proficient()]
        prof_tools = [e["name"] for e in self.equipment.get_proficient()]

        for (prof_type, profs) in [("Armor", prof_armor),
                                   ("Weapons", prof_weapons),
                                   ("Tools", prof_tools)]:
            if len(profs) == 0:
                prof_list.append((prof_type, "None"))
            else:
                prof_list.append((prof_type, ", ".join(profs)))

        return prof_list
