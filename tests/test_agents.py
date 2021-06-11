from dmai.domain.monsters.monster import Monster
import unittest
import sys
import os

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.planning.fast_downward_adapter import FastDownwardAdapter
from dmai.planning.planning_player import PlanningPlayer
from dmai.planning.planning_monster import PlanningMonster
from dmai.agents.monster_agent import MonsterAgent
from dmai.agents.player_agent import PlayerAgent
from dmai.utils.config import Config


class TestPlayerAgent(unittest.TestCase):
    """Test the PlayerAgent class"""
    def setUp(self) -> None:
        Config.agent.set_player("planning")
        Config.planner.set_player("fd")
        self.agent = PlayerAgent(problem="fighter")

    def test_construction(self) -> None:
        self.assertIsInstance(self.agent, PlayerAgent)
        self.assertIsInstance(self.agent.agent, PlanningPlayer)
        self.assertIsInstance(self.agent.agent.planner, FastDownwardAdapter)


class TestMonsterAgent(unittest.TestCase):
    """Test the MonsterAgent class"""
    def setUp(self) -> None:
        Config.agent.set_monster("planning")
        Config.planner.set_monster("fd")
        self.agent = MonsterAgent(problem="giant_rat")

    def test_construction(self) -> None:
        self.assertIsInstance(self.agent, MonsterAgent)
        self.assertIsInstance(self.agent.agent, PlanningMonster)
        self.assertIsInstance(self.agent.agent.planner, FastDownwardAdapter)


if __name__ == "__main__":
    unittest.main()
