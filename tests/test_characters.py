from dmai.game.player import Player
import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.game.state import State
from dmai.utils.output_builder import OutputBuilder
from dmai.domain.characters.character import Character
from dmai.domain.characters.character_collection import CharacterCollection
from dmai.domain.characters.cleric import Cleric
from dmai.domain.characters.fighter import Fighter
from dmai.domain.characters.rogue import Rogue
from dmai.domain.characters.wizard import Wizard


class TestCharacterCollection(unittest.TestCase):
    """Test the CharacterCollection class"""

    def setUp(self) -> None:
        self.character_collection = CharacterCollection()
        self.character_collection.load()
        self.output_builder = OutputBuilder()
        self.state = State(self.output_builder, "")

    def test_character_factory_error(self) -> None:
        with self.assertRaises(ValueError):
            self.character_collection._character_factory(
                "human", self.state, self.output_builder
            )

    def test_get_character_cleric(self) -> None:
        self.assertIsInstance(
            self.character_collection.get_character(
                "cleric", self.state, self.output_builder
            ),
            Cleric,
        )
        self.assertIsInstance(
            self.character_collection.get_character(
                "CLERIC", self.state, self.output_builder
            ),
            Cleric,
        )

    def test_get_character_fighter(self) -> None:
        self.assertIsInstance(
            self.character_collection.get_character(
                "fighter", self.state, self.output_builder
            ),
            Fighter,
        )
        self.assertIsInstance(
            self.character_collection.get_character(
                "FIGHTER", self.state, self.output_builder
            ),
            Fighter,
        )

    def test_get_character_rogue(self) -> None:
        self.assertIsInstance(
            self.character_collection.get_character(
                "rogue", self.state, self.output_builder
            ),
            Rogue,
        )
        self.assertIsInstance(
            self.character_collection.get_character(
                "ROGUE", self.state, self.output_builder
            ),
            Rogue,
        )

    def test_get_character_wizard(self) -> None:
        self.assertIsInstance(
            self.character_collection.get_character(
                "wizard", self.state, self.output_builder
            ),
            Wizard,
        )
        self.assertIsInstance(
            self.character_collection.get_character(
                "WIZARD", self.state, self.output_builder
            ),
            Wizard,
        )

    def test_get_character_wrong(self) -> None:
        self.assertIsNone(
            self.character_collection.get_character(
                "ninja", self.state, self.output_builder
            )
        )


class TestCharacter(unittest.TestCase):
    """Test the Character class and subclasses"""

    def setUp(self) -> None:
        self.character_collection = CharacterCollection()
        self.character_collection.load()
        self.output_builder = OutputBuilder()
        self.state = State(self.output_builder)
        self.fighter = self.character_collection.get_character("fighter", self.state, self.output_builder)
        self.player = Player(self.fighter, self.state, self.output_builder)
        self.state.set_player(self.player)

    def test_character_malformed(self) -> None:
        bad_character1 = {
            "name": "Fighter",
            "char": {"fighter": {"level": 1, "subclass": ""}},
        }
        bad_character2 = {"name": "Fighter", "race": "human"}
        with self.assertRaises(AttributeError):
            Character(bad_character1, self.state, self.output_builder)
        with self.assertRaises(AttributeError):
            Character(bad_character2, self.state, self.output_builder)

    def test_hp_max(self) -> None:
        self.assertEqual(self.fighter.hp_max, 12)

    def test_initiative(self) -> None:
        self.assertEqual(self.fighter.initiative, -1)

    def test_speed(self) -> None:
        self.assertEqual(self.fighter.speed, 30)

    def test_passive_wisdom(self) -> None:
        self.assertEqual(self.fighter.passive_wisdom, 11)

    def test_armor_class(self) -> None:
        self.assertEqual(self.fighter.armor_class, 16)

    def test_darkvision(self) -> None:
        self.assertEqual(self.fighter.has_darkvision(), False)

    def test_has_equipment_good(self) -> None:
        equipment = "torch"
        self.assertEqual(self.fighter.has_equipment(equipment)[0], True)

    def test_has_equipment_bad(self) -> None:
        equipment1 = "rubber_duck"
        equipment2 = "thieves_tools"
        self.assertEqual(self.fighter.has_equipment(equipment1)[0], False)
        self.assertEqual(self.fighter.has_equipment(equipment2)[0], False)

    def test_use_equipment_good(self) -> None:
        equipment = "torch"
        self.assertEqual(True, self.fighter.use_equipment(equipment))

    def test_use_equipment_bad(self) -> None:
        equipment1 = "rubber_duck"
        equipment2 = "thieves_tools"
        self.assertEqual(False, self.fighter.use_equipment(equipment1))
        self.assertEqual(False, self.fighter.use_equipment(equipment2))

    def test_stop_using_equipment_good(self) -> None:
        equipment = "torch"
        self.fighter.use_equipment(equipment)
        self.assertEqual(True, self.fighter.stop_using_equipment(equipment))

    def test_stop_using_equipment_bad(self) -> None:
        equipment1 = "rubber_duck"
        equipment2 = "thieves_tools"
        self.assertEqual(False, self.fighter.stop_using_equipment(equipment1))
        self.assertEqual(False, self.fighter.stop_using_equipment(equipment2))

    def test_can_equip_good(self) -> None:
        weapon = "greataxe"
        self.fighter.unequip_weapon()
        self.assertEqual(True, self.fighter.can_equip(weapon)[0])

    def test_can_equip_bad(self) -> None:
        weapon1 = "rubber_duck"
        weapon2 = "scimitar"
        self.fighter.unequip_weapon()
        self.assertEqual(False, self.fighter.can_equip(weapon1)[0])
        self.assertEqual(False, self.fighter.can_equip(weapon2)[0])

    def test_can_unequip_good(self) -> None:
        weapon = "greataxe"
        self.assertEqual(True, self.fighter.can_unequip(weapon)[0])

    def test_can_unequip_bad(self) -> None:
        weapon1 = "rubber_duck"
        weapon2 = "scimitar"
        self.assertEqual(False, self.fighter.can_unequip(weapon1)[0])
        self.assertEqual(False, self.fighter.can_unequip(weapon2)[0])

    def test_is_equipped_good(self) -> None:
        weapon = "greataxe"
        self.assertEqual(True, self.fighter.is_equipped(weapon))

    def test_is_equipped_bad(self) -> None:
        weapon1 = "rubber_duck"
        weapon2 = "scimitar"
        self.assertEqual(False, self.fighter.is_equipped(weapon1))
        self.assertEqual(False, self.fighter.is_equipped(weapon2))

    def test_equip_weapon_good(self) -> None:
        weapon1 = "greataxe"
        self.assertEqual(True, self.fighter.equip_weapon(weapon1))

    def test_equip_weapon_bad(self) -> None:
        weapon1 = "rubber_duck"
        weapon2 = "scimitar"
        self.assertEqual(False, self.fighter.equip_weapon(weapon1))
        self.assertEqual(False, self.fighter.equip_weapon(weapon2))

    def test_unequip_weapon_good(self) -> None:
        weapon1 = "greataxe"
        self.assertEqual(True, self.fighter.unequip_weapon(weapon1))

    def test_unequip_weapon_bad(self) -> None:
        weapon1 = "rubber_duck"
        weapon2 = "scimitar"
        self.assertEqual(False, self.fighter.unequip_weapon(weapon1))
        self.assertEqual(False, self.fighter.unequip_weapon(weapon2))

    def test_get_proficiencies_skills(self) -> None:
        prof_type = "skills"
        skill_profs = ["athletics", "history"]
        self.assertListEqual(skill_profs, self.fighter.get_proficiencies(prof_type))

    def test_get_proficiencies_armor(self) -> None:
        prof_type = "armor"
        armor_profs = ["light", "medium", "heavy", "shield"]
        self.assertListEqual(armor_profs, self.fighter.get_proficiencies(prof_type))

    def test_get_proficiencies_bad(self) -> None:
        prof_type = "ducks"
        self.assertListEqual([], self.fighter.get_proficiencies(prof_type))

    def test_get_class(self) -> None:
        self.assertEqual(self.fighter.get_class(), "Fighter 1")

    def test_get_race(self) -> None:
        self.assertEqual(self.fighter.get_race(), "Human")

    def test_get_alignment(self) -> None:
        self.assertEqual(self.fighter.get_alignment(), "Lawful neutral")

    def test_get_ability_score(self) -> None:
        ability = "dex"
        self.assertEqual(self.fighter.get_ability_score(ability), 9)

    def test_get_ability_modifier(self) -> None:
        ability = "dex"
        self.assertEqual(self.fighter.get_ability_modifier(ability), -1)

    def test_get_skill_modifier(self) -> None:
        ability = "athletics"
        self.assertEqual(self.fighter.get_skill_modifier(ability), 5)

    def test_get_signed_attack_bonus_fighter(self) -> None:
        weapon1 = "dagger"
        weapon2 = "greataxe"
        self.assertEqual(self.fighter.get_signed_attack_bonus(weapon1), "+5")
        self.assertEqual(self.fighter.get_signed_attack_bonus(weapon2), "+5")

    def test_get_saving_throw(self) -> None:
        ability1 = "str"
        ability2 = "cha"
        self.assertEqual(self.fighter.get_saving_throw(ability1), 5)
        self.assertEqual(self.fighter.get_saving_throw(ability2), 2)

    def test_get_formatted_ability(self) -> None:
        ability1 = "str"
        ability2 = "cha"
        self.assertEqual(self.fighter.get_formatted_ability(ability1), "+3 (16)")
        self.assertEqual(self.fighter.get_formatted_ability(ability2), "+2 (14)")

    def test_get_formatted_saving_throw(self) -> None:
        ability1 = "str"
        ability2 = "cha"
        self.assertEqual(
            self.fighter.get_formatted_saving_throw(ability1), "+5 (proficiency)"
        )
        self.assertEqual(self.fighter.get_formatted_saving_throw(ability2), "+2")

    def test_get_formatted_skill_modifier(self) -> None:
        skill1 = "athletics"
        skill2 = "stealth"
        self.assertEqual(
            self.fighter.get_formatted_skill_modifier(skill1), "+5 (proficiency)"
        )
        self.assertEqual(self.fighter.get_formatted_skill_modifier(skill2), "-1")

    def test_get_formatted_speed(self) -> None:
        self.assertEqual(self.fighter.get_formatted_speed(), "30 ft")

    def test_get_formatted_armor(self) -> None:
        self.assertEqual(self.fighter.get_formatted_armor(), "Chain mail (equipped)")

    def test_get_formatted_proficiencies(self) -> None:
        profs = self.fighter.get_formatted_proficiencies()
        self.assertTupleEqual(
            ("Armor", "Leather, Padded, Scale mail, Chain mail, Shield"), profs[0]
        )
        self.assertTupleEqual(
            (
                "Weapons",
                "Dagger, Handaxe, Javelin, Quarterstaff, Light crossbow, Shortbow, Greataxe, Scimitar, Shortsword, Warhammer",
            ),
            profs[1],
        )
        self.assertTupleEqual(("Tools", "None"), profs[2])

    def test_get_formatted_languages(self) -> None:
        self.assertEqual(self.fighter.get_formatted_languages(), "Common and Dwarvish")


if __name__ == "__main__":
    unittest.main()
