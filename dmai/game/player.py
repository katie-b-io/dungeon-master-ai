from dmai.domain.characters.character import Character
from dmai.domain.skills import Skills
from dmai.domain.abilities import Abilities


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
        char_str += div
        char_str += "{l:<20} {v:<30}\n".format(l="Abilities:", v="Modifier (score)")
        for (ability, name) in Abilities.get_all_abilities():
            char_str += "{l:<20} {v:<30}\n".format(
                l=name + ":", v=self.character.get_formatted_ability(ability)
            )

        char_str += div
        char_str += "{l:<20} {v:<30}\n".format(
            l="Saving throws:", v="Modifier (proficiency)"
        )
        for (ability, name) in Abilities.get_all_abilities():
            char_str += "{l:<20} {v:<30}\n".format(
                l=name + ":", v=self.character.get_formatted_saving_throw(ability)
            )

        char_str += div
        char_str += "{l:<20} {v:<30}\n".format(
            l="Skills:", v="Modifier (proficiency/expertise)"
        )
        for (skill, name) in Skills.get_all_skills():
            char_str += "{l:<20} {v:<30}\n".format(
                l=name + ":", v=self.character.get_formatted_skill_modifier(skill)
            )

        char_str += div
        return char_str
