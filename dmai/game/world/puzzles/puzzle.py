from abc import ABC, abstractmethod

from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class Puzzle(ABC):
    def __init__(self, puzzle_data: dict) -> None:
        """Puzzle abstract class"""
        self.solved = False
        self.triggered = False
        try:
            for key in puzzle_data:
                self.__setattr__(key, puzzle_data[key])
        except AttributeError as e:
            logger.error(
                "Cannot create puzzle, incorrect attribute: {e}".format(e=e))
            raise

    def __repr__(self) -> str:
        return "{c}: {n}".format(c=self.__class__.__name__, n=self.name)

    def solve(self) -> None:
        self.solved = True

    def trigger(self) -> None:
        self.triggered = True

    def get_solution(self, solution: str) -> dict:
        """Method to return specified solution details"""
        return self.solutions[solution]

    def get_all_solutions(self) -> list:
        """Method to return possible solutions to puzzle"""
        return self.solutions

    def check_solution(self, solution: str) -> bool:
        """Method to determine if possible solution exists.
        Returns bool"""
        return solution in self.solutions

    def check_solution_ability(self, ability: str) -> bool:
        """Method to determine if possible ability solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "ability" in s:
                if ability == s["ability"]:
                    return True

    def check_solution_skill(self, skill: str) -> bool:
        """Method to determine if possible skill solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "skill" in s:
                if skill == s["skill"]:
                    return True

    def check_solution_item(self, item: str) -> bool:
        """Method to determine if possible item solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "item" in s:
                if item == s["item"]:
                    return True

    def check_solution_equipment(self, equipment: str) -> bool:
        """Method to determine if possible equipment solution exists.
        Returns bool"""
        for s in self.solutions.values():
            if "equipment" in s:
                if equipment == s["equipment"]:
                    return True
