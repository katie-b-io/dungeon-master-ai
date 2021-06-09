from subprocess import run, PIPE
import os

from dmai.planning.planner_adapter import PlannerAdapter
from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class FastDownwardAdapter(PlannerAdapter):
    def __init__(self, domain: str, problem: str) -> None:
        """FastDownwardAdapter class"""
        PlannerAdapter.__init__(self, domain, problem)

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def build_plan(self) -> bool:
        """Build a plan using FastDownward.
        Returns boolean indicating successful execution"""
        logger.debug("Building plan with FastDownward")
        domain_file = os.path.join(
            Config.directory.planning,
            "{u}.{d}.domain.pddl".format(u=Config.uuid, d=self.domain))
        problem_file = os.path.join(
            Config.directory.planning,
            "{u}.{p}.problem.pddl".format(u=Config.uuid, p=self.problem))
        plan_file = os.path.join(
            Config.directory.planning,
            "{u}.{d}-{p}.plan".format(u=Config.uuid,
                                      d=self.domain,
                                      p=self.problem))
        p = run([
            'fast-downward.py', '--plan-file', plan_file, domain_file,
            problem_file, '--search', 'astar(add())'
        ],
                      stdout=PIPE,
                      stderr=PIPE,
                      universal_newlines=True)
        logger.debug(p.stdout)
        logger.debug(p.stderr)
        
        return p.returncode == 0

    def parse_plan(self) -> list:
        """Reads the plan file and returns a list"""
        plan_file = os.path.join(
            Config.directory.planning,
            "{u}.{d}-{p}.plan".format(u=Config.uuid,
                                      d=self.domain,
                                      p=self.problem))
        with open(plan_file, 'r') as reader:
            plan = reader.readlines()

        return plan