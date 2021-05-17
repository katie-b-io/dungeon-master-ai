from dmai.domain.characters.character import Character
from dmai.domain.skills import Skills
from dmai.domain.abilities import Abilities
from dmai.game.state import State


class Player:
    def __init__(self, character: Character) -> None:
        """Main class for the player"""
        self.name = None
        self.character = character

    def set_name(self, name: str) -> None:
        self.name = name

    @property
    def character_class(self) -> str:
        return self.character.name

    def get_character_sheet(self) -> str:
        """Method to return a properly formatted character sheet"""
        div = "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

        # Character background
        char_str = div
        char_str += "Character Sheet:\n"
        char_str += "{l:<20} {v:<30}\n".format(l="Name:", v=self.name)
        char_str += "{l:<20} {v:<30}\n".format(
            l="Class & level:", v=self.character.get_class()
        )
        char_str += "{l:<20} {v:<30}\n".format(l="Race:", v=self.character.get_race())
        char_str += "{l:<20} {v:<30}\n".format(
            l="Alignment:", v=self.character.get_alignment()
        )

        # Character stats
        char_str += div
        char_str += "Stats:\n"
        char_str += "{l:<20} {v:<30}\n".format(
            l="Armor class:", v=self.character.armor_class
        )
        char_str += "{l:<20} {v:<30}\n".format(
            l="Initiative:", v=self.character.get_signed_initiative()
        )
        char_str += "{l:<20} {v:<30}\n".format(
            l="Speed:", v=self.character.get_formatted_speed()
        )

        # Health
        char_str += div
        char_str += "Health:\n"
        char_str += "{l:<20} {v:<30}\n".format(
            l="Hit point maximum:", v=self.character.hp_max
        )
        char_str += "{l:<20} {v:<30}\n".format(
            l="Current hit points:", v=State.get_current_hp()
        )

        # Abilities
        char_str += div
        char_str += "{l:<20} {v:<30}\n".format(l="Abilities:", v="Modifier (score)")
        for (ability, name) in Abilities.get_all_abilities():
            char_str += "{l:<20} {v:<30}\n".format(
                l=name + ":", v=self.character.get_formatted_ability(ability)
            )

        # Saving throws
        char_str += div
        char_str += "{l:<20} {v:<30}\n".format(
            l="Saving throws:", v="Modifier (proficiency)"
        )
        for (ability, name) in Abilities.get_all_abilities():
            char_str += "{l:<20} {v:<30}\n".format(
                l=name + ":", v=self.character.get_formatted_saving_throw(ability)
            )

        # Skills
        char_str += div
        char_str += "{l:<20} {v:<30}\n".format(
            l="Skills:", v="Modifier (proficiency/expertise)"
        )
        for (skill, name) in Skills.get_all_skills():
            char_str += "{l:<20} {v:<30}\n".format(
                l=name + ":", v=self.character.get_formatted_skill_modifier(skill)
            )

        # Attacks
        char_str += div
        char_str += "{l:<20} {v:<20} {t:<30}\n".format(
            l="Attacks:", v="Attack bonus", t="Damage (type)"
        )
        for (weapon, name) in self.character.get_all_weapons():
            char_str += "{l:<20} {a:<20} {v:<30}\n".format(
                l=name + ":",
                a=self.character.get_signed_attack_bonus(weapon),
                v=self.character.get_formatted_attack(weapon),
            )
            
        # Equipment
        char_str += div
        char_str += "Equipment:\n"
        char_str += "{e}\n".format(e=self.character.get_formatted_equipment())

        # Money
        char_str += div
        char_str += "Money:\n"
        char_str += "{m}\n".format(m=self.character.get_formatted_money())
        
        # Languages
        char_str += div
        char_str += "Languages:\n"
        char_str += "{l}\n".format(l=self.character.get_formatted_languages())
        
        # Proficiencies
        char_str += div
        char_str += "Proficiencies:\n"
        for (prof_type, profs) in self.character.get_formatted_proficiencies():
            char_str += "{l:<20} {v:<30}\n".format(
                l=prof_type + ":",
                v=profs,
            )
            
        # Features
        char_str += div
        char_str += "Features:\n"
        for (feature, name) in self.character.get_all_features():
            char_str += "{l:<25} {v:<30}\n".format(
                l=name + ":", v=self.character.get_feature_description(feature, indent_length=26)
            )
        
        char_str += div
        return char_str
