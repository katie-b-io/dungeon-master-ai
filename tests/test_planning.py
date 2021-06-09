import unittest
import sys
import os
import shutil

p = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, p + "/../")

from dmai.planning.fast_downward_adapter import FastDownwardAdapter
from dmai.utils.config import Config


class TestFastDownwardAdapter(unittest.TestCase):
    """Test the FastDownwardAdapter class"""
    def setUp(self) -> None:
        self.domain = "player_domain"
        self.problem = "player_problem_fighter"
        try:
            Config.set_uuid()
            shutil.copy(
                os.path.join(Config.directory.planning_test,
                             "{d}.pddl".format(d=self.domain)),
                os.path.join(
                    Config.directory.planning,
                    "{u}.{d}.domain.pddl".format(d=self.domain, u=Config.uuid)))
            shutil.copy(
                os.path.join(Config.directory.planning_test,
                             "{p}.pddl".format(p=self.problem)),
                os.path.join(
                    Config.directory.planning,
                    "{u}.{p}.problem.pddl".format(p=self.problem, u=Config.uuid)))
            self.adapter = FastDownwardAdapter(self.domain, self.problem)
        except Exception:
            self.tearDown()

    def tearDown(self) -> None:
        os.remove(
            os.path.join(Config.directory.planning,
                         "{u}.{d}.domain.pddl".format(d=self.domain, u=Config.uuid)))
        os.remove(
            os.path.join(Config.directory.planning,
                         "{u}.{p}.problem.pddl".format(p=self.problem, u=Config.uuid)))
        os.remove(
            os.path.join(
                Config.directory.planning,
                "{u}.{d}-{p}.plan".format(d=self.domain,
                                          p=self.problem,
                                          u=Config.uuid)))

    def test_build_plan(self) -> None:
        p = self.adapter.build_plan()
        self.assertEqual(p, True)


if __name__ == "__main__":
    unittest.main()
