import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + '/../')

from dmai.utils import DiceRoller, Loader

class TestDiceRoller(unittest.TestCase):
    '''Test the DiceRoller class'''
    def setUp(self) -> None:
        self.dice = {
            "d4": {
                "specs": {
                    "die": "d4",
                    "total": 2,
                    "mod": 1
                },
                "min": 3,
                "max": 9
            },
            "d6": {
                "specs": {
                    "die": "d6",
                    "total": 3,
                    "mod": 2
                },
                "min": 5,
                "max": 20
            },
            "d8": {
                "specs": {
                    "die": "d8",
                    "total": 3,
                    "mod": 2
                },
                "min": 5,
                "max": 26
            },
            "d12": {
                "specs": {
                    "die": "d12",
                    "total": 3,
                    "mod": 3
                },
                "min": 6,
                "max": 39
            },
            "d20": {
                "specs": {
                    "die": "d20",
                    "total": 2,
                    "mod": 2
                },
                "min": 4,
                "max": 42
            }
        }
        
    def test_roll_die(self) -> None:
        bad_die1 = "d3"
        bad_die2 = "20"
        with self.assertRaises(KeyError):
            DiceRoller.roll_die(bad_die1)
        with self.assertRaises(KeyError):
            DiceRoller.roll_die(bad_die2)
            
    def test_roll_dice_d4(self) -> None:
        # roll D4 600 times
        total_rolls = 600
        rolls = [DiceRoller.roll_dice(self.dice["d4"]["specs"]) for _ in range(total_rolls)]
        self.assertGreaterEqual(min(rolls), self.dice["d4"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d4"]["max"])
        self.assertAlmostEqual(rolls.count(self.dice["d4"]["min"])/total_rolls,
                               rolls.count(self.dice["d4"]["max"])/total_rolls,
                               places=1)

    def test_roll_dice_d6(self) -> None:
        # roll D6 600 times
        total_rolls = 600
        rolls = [DiceRoller.roll_dice(self.dice["d6"]["specs"]) for _ in range(total_rolls)]
        self.assertGreaterEqual(min(rolls), self.dice["d6"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d6"]["max"])
        self.assertAlmostEqual(rolls.count(self.dice["d6"]["min"])/total_rolls,
                               rolls.count(self.dice["d6"]["max"])/total_rolls,
                               places=1)
        
    def test_roll_dice_d8(self) -> None:
        # roll d8 600 times
        total_rolls = 600
        rolls = [DiceRoller.roll_dice(self.dice["d8"]["specs"]) for _ in range(total_rolls)]
        self.assertGreaterEqual(min(rolls), self.dice["d8"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d8"]["max"])
        self.assertAlmostEqual(rolls.count(self.dice["d8"]["min"])/total_rolls,
                               rolls.count(self.dice["d8"]["max"])/total_rolls,
                               places=1)
        
    def test_roll_dice_d12(self) -> None:
        # roll D12 600 times
        total_rolls = 600
        rolls = [DiceRoller.roll_dice(self.dice["d12"]["specs"]) for _ in range(total_rolls)]
        self.assertGreaterEqual(min(rolls), self.dice["d12"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d12"]["max"])
        self.assertAlmostEqual(rolls.count(self.dice["d12"]["min"])/total_rolls,
                               rolls.count(self.dice["d12"]["max"])/total_rolls,
                               places=1)
        
    def test_roll_dice_d20(self) -> None:
        # roll D20 600 times
        total_rolls = 600
        rolls = [DiceRoller.roll_dice(self.dice["d20"]["specs"]) for _ in range(total_rolls)]
        self.assertGreaterEqual(min(rolls), self.dice["d20"]["min"])
        self.assertLessEqual(max(rolls), self.dice["d20"]["max"])
        self.assertAlmostEqual(rolls.count(self.dice["d20"]["min"])/total_rolls,
                               rolls.count(self.dice["d20"]["max"])/total_rolls,
                               places=1)
        
    def test_roll_dice_malformed(self) -> None:
        bad_spec1 = {
            "die": "d3",
            "total": 1,
            "mod": 2
        }
        bad_spec2 = {
            "die": "d4",
            "total": 1
        }
        bad_spec3 = {
            "type": "d4",
            "total": 1,
            "mod": 0
        }
        bad_spec4 = {
            "die": "d4",
            "total": "1",
            "mod": 0
        }
        with self.assertRaises(KeyError):
            DiceRoller.roll_dice(bad_spec1)
        with self.assertRaises(KeyError):
            DiceRoller.roll_dice(bad_spec2)
        with self.assertRaises(KeyError):
            DiceRoller.roll_dice(bad_spec3)
        with self.assertRaises(TypeError):
            DiceRoller.roll_dice(bad_spec4)
    
if __name__ == "__main__":
    unittest.main()