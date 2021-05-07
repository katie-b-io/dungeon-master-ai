import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.dm import DM
from dmai.domain.characters import Fighter

class TestDM(unittest.TestCase):
    """Test the DM class"""

    def setUp(self) -> None:
        self.dm = DM("the_tomb_of_baradin_stormfury")

    def test_init(self) -> None:
        self.assertIn("monsters", self.dm.__dict__)
        self.assertIn("characters", self.dm.__dict__)

    def test_get_character(self) -> None:
        self.assertIsInstance(self.dm.get_character("fighter"), Fighter)
        self.assertIsInstance(self.dm.get_character("FIGHTER"), Fighter)
        
if __name__ == "__main__":
    unittest.main()