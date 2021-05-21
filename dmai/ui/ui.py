from dmai.utils.output_builder import OutputBuilder
from dmai.game.game import Game
from dmai.game.state import State


class UserInterface:
    def __init__(self, game: Game) -> None:
        """UserInterface class for the game and interacting with the DM"""
        self.game = game

    def execute(self) -> None:
        """Execute function which allows CLI communication between
        player and DM"""
        while True:
            OutputBuilder.append(self.game.output())
            output = OutputBuilder.format()
            if output:
                prompt = "\n" + output + "\n"
            else:
                prompt = "\n"
            
            if State.in_combat:
                prompt += "[COMBAT] "
            
            prompt += "> "
            if State.paused:
                prompt += "Press enter to continue... "
            
            user_input = input(prompt)
            OutputBuilder.clear()
            self.game.input(user_input)
