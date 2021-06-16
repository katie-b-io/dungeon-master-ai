from dmai.domain.monsters.monster import Monster
import unittest
import sys
import os
import shutil

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.planning.fast_downward_adapter import FastDownwardAdapter
from dmai.planning.planning_player import PlanningPlayer
from dmai.planning.planning_monster import PlanningMonster
from dmai.agents.monster_agent import MonsterAgent
from dmai.agents.player_agent import PlayerAgent
from dmai.utils.config import Config
from dmai.game.game import Game


class TestPlayerAgent(unittest.TestCase):
    """Test the PlayerAgent class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter",
                         char_name="Xena",
                         adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        Config.set_uuid()
        Config.agent.set_player("planning")
        Config.planner.set_player("fd")
        self.problem = "fighter"
        self.agent = PlayerAgent(problem=self.problem)

    def tearDown(self) -> None:
        shutil.rmtree(Config.directory.planning)

    def test_construction(self) -> None:
        self.assertIsInstance(self.agent, PlayerAgent)
        self.assertIsInstance(self.agent.agent, PlanningPlayer)
        self.assertIsInstance(self.agent.agent.planner, FastDownwardAdapter)

    def test_get_agent(self) -> None:
        self.assertIsInstance(self.agent.get_agent(problem=self.problem),
                              PlanningPlayer)

    def test_prepare_next_move(self) -> None:
        succeed = self.agent.prepare_next_move()
        self.assertEqual(True, succeed)

    def test_print_next_move(self) -> None:
        self.agent.prepare_next_move()
        move = self.agent.print_next_move()
        self.assertEqual(True, move)


class TestMonsterAgent(unittest.TestCase):
    """Test the MonsterAgent class"""
    def setUp(self) -> None:
        self.game = Game(char_class="fighter",
                         char_name="Xena",
                         adventure="the_tomb_of_baradin_stormfury")
        self.game.load()
        Config.set_uuid()
        Config.agent.set_monster("planning")
        Config.planner.set_monster("fd")
        self.problem = "giant_rat"
        self.agent = MonsterAgent(problem=self.problem)

    def tearDown(self) -> None:
        shutil.rmtree(Config.directory.planning)

    def test_construction(self) -> None:
        self.assertIsInstance(self.agent, MonsterAgent)
        self.assertIsInstance(self.agent.agent, PlanningMonster)
        self.assertIsInstance(self.agent.agent.planner, FastDownwardAdapter)

    def test_get_agent(self) -> None:
        self.assertIsInstance(self.agent.get_agent(problem=self.problem),
                              PlanningMonster)

    def test_prepare_next_move(self) -> None:
        succeed = self.agent.prepare_next_move()
        self.assertEqual(True, succeed)

    def test_print_next_move(self) -> None:
        self.agent.prepare_next_move()
        move = self.agent.print_next_move()
        self.assertEqual(False, move)


if __name__ == "__main__":
    unittest.main()
