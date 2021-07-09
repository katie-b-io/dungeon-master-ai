import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.nlg.nlg import NLG
from dmai.game.game import Game
from dmai.domain.items.potion_of_healing import PotionOfHealing


class TestPotionOfHealing(unittest.TestCase):
    """Test the PotionOfHealing"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter",
                         char_name="Xena",
                         adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        item_data = {
            "name": "Potion of Healing",
            "type": "potion",
            "rarity": "common",
            "value": 5000,
            "description": "A character who drinks the magical red fluid in this vial regains 2d4 + 2 hit points. Drinking or administering a potion takes an action.",
            "effects": {
                "hit_point": {
                    "delta": {
                        "type": "increase",
                        "die": "d4",
                        "total": 2,
                        "mod": 2
                    }
                }
            }
        }
        self.potion = PotionOfHealing(item_data, self.game.state, self.game.output_builder)
    
    def test_use(self) -> None:
        starting_hp = 1
        self.game.state.current_hp["player"] = starting_hp
        self.potion.use()
        self.assertGreater(self.game.state.get_current_hp(), starting_hp)

        
if __name__ == "__main__":
    unittest.main()
