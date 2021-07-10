from subprocess import run, PIPE
import os

from dmai.game.state import State
from dmai.utils.output_builder import OutputBuilder
from dmai.planning.planner_adapter import PlannerAdapter
from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class FastDownwardAdapter(PlannerAdapter):
    def __init__(self, domain: str, problem: str, state: State, output_builder: OutputBuilder) -> None:
        """FastDownwardAdapter class"""
        PlannerAdapter.__init__(self, domain, problem, state, output_builder)

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def build_plan(self) -> bool:
        """Build a plan using FastDownward.
        Returns boolean indicating successful execution"""
        logger.debug("Building plan with FastDownward")
        domain_file = os.path.join(
            Config.directory.planning,
            "{u}.{d}.domain.pddl".format(u=self.state.session.session_id, d=self.domain))
        problem_file = os.path.join(
            Config.directory.planning,
            "{u}.{p}.problem.pddl".format(u=self.state.session.session_id, p=self.problem))
        plan_file = os.path.join(
            Config.directory.planning,
            "{u}.{d}-{p}.plan".format(u=self.state.session.session_id,
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

    def parse_plan(self) -> None:
        """Reads the plan file, saves to self.plan"""
        plan_file = os.path.join(
            Config.directory.planning,
            "{u}.{d}-{p}.plan".format(u=self.state.session.session_id,
                                      d=self.domain,
                                      p=self.problem))
        with open(plan_file, 'r') as reader:
            plan = reader.readlines()
        
        # remove the footer line
        if "; cost = 0 (unit cost)" in plan[-1]:
            del plan[-1]

        self.plan = plan