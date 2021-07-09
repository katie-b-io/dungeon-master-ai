from dmai.game.world.puzzles.puzzle import Puzzle
from dmai.game.state import State


class PuzzleCollection:
    def __init__(self, puzzles_dict: dict, state: State) -> None:
        """PuzzleCollection class"""
        self.puzzles = {}
        self.state = state

        # prepare the puzzles
        for puzzle_id in puzzles_dict:
            puzzle = Puzzle(puzzles_dict[puzzle_id], self.state)
            self.puzzles[puzzle_id] = puzzle

    def __repr__(self) -> str:
        return "Puzzle collection:\n{a}".format(a=self.puzzles)

    def get_all_puzzles(self) -> list:
        """Method to return a list of all puzzles"""
        return list(self.puzzles.values())
    
    def get_puzzle(self, puzzle_id: str) -> Puzzle:
        """Method to return a specified puzzle"""
        if puzzle_id in self.puzzles:
            return self.puzzles[puzzle_id]
    
    def can_attack_door(self, room: str, door: str) -> bool:
        """Method to return whether a door of room can be attacked"""
        door_id = "{i}---{d}".format(i=room, d=door)
        return bool(door_id in self.puzzles)
    
    def get_door_armor_class(self, room: str, door: str) -> int:
        """Method to return the armor class of specified door"""
        if self.can_attack_door(room, door):
            door_id = "{i}---{d}".format(i=room, d=door)
            return self.puzzles[door_id].get_armor_class()

    def get_door_hp(self, room: str, door: str) -> int:
        """Method to return the armor class of specified door"""
        if self.can_attack_door(room, door):
            door_id = "{i}---{d}".format(i=room, d=door)
            return self.puzzles[door_id].get_hp()
    
    def explore_trigger(self) -> None:
        """Method to print any new text if conditions met"""
        for puzzle in self.get_all_puzzles():
            puzzle.explore_trigger()