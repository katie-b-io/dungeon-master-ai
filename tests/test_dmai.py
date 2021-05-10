import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.dm import DM
from dmai.domain.characters.fighter import Fighter

class TestDM(unittest.TestCase):
    """Test the DM class"""

    def setUp(self) -> None:
        self.dm = DM("the_tomb_of_baradin_stormfury")

    def test_init(self) -> None:
        self.assertIn("adventure", self.dm.__dict__)
        
if __name__ == "__main__":
    unittest.main()