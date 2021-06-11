from dmai.game.world.puzzles.puzzle import Puzzle


class PuzzleCollection:
    def __init__(self, puzzles_dict: dict) -> None:
        """PuzzleCollection class"""
        self.puzzles = dict()

        # prepare the puzzles
        for puzzle_id in puzzles_dict:
            puzzle = Puzzle(puzzles_dict[puzzle_id])
            self.puzzles[puzzle_id] = puzzle

    def __repr__(self) -> str:
        return "Puzzle collection:\n{a}".format(a=self.puzzles)

    def get_all_puzzles(self) -> list:
        """Method to return a list of all puzzles"""
        return list(self.puzzles.values())