import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + '/../')

from dmai.domain import Domain, Skills
from dmai.domain.characters import Fighter

class TestDomain(unittest.TestCase):
    '''Test the Domain class'''
    def setUp(self) -> None:
        self.domain = Domain()
    
    def test_load_all(self) -> None:
        self.domain.load_all()
        self.assertIn("monsters", self.domain.__dict__)
        self.assertIn("characters", self.domain.__dict__)
        
    def test_get_character(self) -> None:
        self.domain.load_all()
        self.assertIsInstance(self.domain.get_character("fighter"), Fighter)
        self.assertIsInstance(self.domain.get_character("FIGHTER"), Fighter)
    
if __name__ == "__main__":
    unittest.main()