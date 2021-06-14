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
    def _prepare_adapter(self, domain: str,
                         problem: str) -> FastDownwardAdapter:
        shutil.copy(
            os.path.join(Config.directory.planning_test,
                         "{d}.pddl".format(d=domain)),
            os.path.join(Config.directory.planning,
                         "{u}.{d}.domain.pddl".format(d=domain,
                                                      u=Config.uuid)))
        shutil.copy(
            os.path.join(Config.directory.planning_test,
                         "{p}.pddl".format(p=problem)),
            os.path.join(
                Config.directory.planning,
                "{u}.{p}.problem.pddl".format(p=problem, u=Config.uuid)))
        return FastDownwardAdapter(domain, problem)

    def _cleanup(self, domain, problem) -> None:
            os.remove(
                os.path.join(
                    Config.directory.planning,
                    "{u}.{d}.domain.pddl".format(d=domain, u=Config.uuid)))
            os.remove(
                os.path.join(
                    Config.directory.planning,
                    "{u}.{p}.problem.pddl".format(p=problem, u=Config.uuid)))
            os.remove(
                os.path.join(
                    Config.directory.planning,
                    "{u}.{d}-{p}.plan".format(d=domain,
                                              p=problem,
                                              u=Config.uuid)))

    def test_build_plan_player(self) -> None:
        domain = "player_domain"
        problem = "player_problem_fighter"
        try:
            Config.set_uuid()
            adapter = self._prepare_adapter(domain, problem)
            p = adapter.build_plan()
        except Exception:
            self._cleanup(domain, problem)
        self.assertEqual(p, True)
        self._cleanup(domain, problem)

    def test_build_plan_monster(self) -> None:
        domain = "monster_domain"
        problem = "monster_problem_inns_cellar"
        try:
            Config.set_uuid()
            adapter = self._prepare_adapter(domain, problem)
            m = adapter.build_plan()
        except Exception:
            self._cleanup(domain, problem)
        self.assertEqual(m, True)
        self._cleanup(domain, problem)


if __name__ == "__main__":
    unittest.main()
