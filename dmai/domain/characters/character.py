from abc import ABC

from dmai.domain.abilities import Abilities
from dmai.domain.alignment import Alignment
from dmai.domain.armor import Armor
from dmai.domain.attacks import Attacks
from dmai.domain.conditions import Conditions
from dmai.domain.equipment import Equipment
from dmai.domain.features import Features
from dmai.domain.languages import Languages
from dmai.domain.skills import Skills
from dmai.domain.spells import Spells
from dmai.domain.characters.character_class import CharacterClass
from dmai.domain.characters.race import Race
from dmai.utils.dice_roller import DiceRoller


class Character(ABC):
    def __init__(self, character_data: dict) -> None:
        """Character abstract class"""
        self.name = None

        try:
            for key in character_data:
                self.__setattr__(key, character_data[key])

            # replace the attributes values with objects where appropriate
            self.abilities = Abilities(self.abilities)
            self.alignment = Alignment(self.alignment)
            self.armor = Armor(self.armor)
            self.attacks = Attacks()
            self.char_class = CharacterClass(self.char_class)
            self.conditions = Conditions()
            self.equipment = Equipment(self.equipment)
            self.languages = Languages(self.languages)
            self.race = Race(self.race)
            self.skills = Skills(
                abilities=self.abilities,
                pro_bonus=self.proficiency_bonus,
                proficiencies=self.proficiencies["skills"],
            )
            self.spells = Spells(self.spells)
            self.features = Features(char_class=self.char_class, race=self.race)

        except AttributeError as e:
            print("Cannot create character, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "Character: {n}\nMax HP: {hp}".format(n=self.name, hp=self.hp_max)

    @property
    def hp_max(self) -> int:
        """Method to return the maximum hit points"""
        hp = DiceRoller.get_max(self.char_class.hit_dice)
        mod = self.abilities.get_modifier("con")
        return hp + mod

    @property
    def passive_wisdom(self) -> int:
        """Method to return the passive wisdom attribute"""
        return 10 + self.abilities.get_modifier("wis")

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

    def get_formatted_ability(self, ability: str) -> str:
        """Method to return the specified ability string"""
        return "{m} ({a})".format(
            m=self.get_ability_modifier(ability), a=self.get_ability_score(ability)
        )

    def get_saving_throw(self, ability: str) -> int:
        """Method to return the specified saving throw"""
        if ability in self.char_class.proficiencies["saving_throws"]:
            return self.proficiency_bonus + self.get_ability_modifier(ability)
        else:
            return self.get_ability_modifier(ability)

    def get_formatted_saving_throw(self, ability: str) -> str:
        """Method to return the specified saving throw formatted string"""
        if ability in self.char_class.proficiencies["saving_throws"]:
            return "{s} (proficiency)".format(s=self.get_saving_throw(ability))
        else:
            return "{s}".format(s=self.get_saving_throw(ability))

    def get_skill_modifier(self, skill: str) -> int:
        """Method to return the specified skill modifier"""
        return self.skills.get_modifier(skill)

    def get_formatted_skill_modifier(self, skill: str) -> str:
        """Method to return the specified skill modifier formatted string"""
        if (
            "expertise" in self.proficiencies["skills"]
            and skill in self.proficiencies["skills"]["expertise"]
        ):
            return "{m} (expertise)".format(m=self.get_skill_modifier(skill))
        elif skill in self.proficiencies["skills"]["class"]:
            return "{m} (proficiency)".format(m=self.get_skill_modifier(skill))
        else:
            return "{m}".format(m=self.get_skill_modifier(skill))
