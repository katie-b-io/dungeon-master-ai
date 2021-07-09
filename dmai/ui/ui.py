from dmai.game.game import Game
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class UserInterface:
    def __init__(self, game: Game) -> None:
        """UserInterface class for the game and interacting with the DM"""
        self.game = game

    def execute(self) -> None:
        """Execute function which allows CLI communication between
        player and DM"""
        while True:
            output = self.game.output()
            logger.info("[DM]: {o}".format(o=output))

            if output:
                prompt = "\n" + output + "\n"
            else:
                prompt = "\n"

            if self.game.state.in_combat:
                prompt += "[COMBAT] "

            prompt += "> "
            if self.game.state.paused:
                prompt += "Press enter to continue... "

            user_input = input(prompt)
            logger.info("[PLAYER]: {i}".format(i=user_input))
            self.game.input(user_input)

    def input(self, user_input: str) -> None:
        """Input the user input"""
        logger.info("[PLAYER]: {i}".format(i=user_input))
        self.game.input(user_input)
    
    def output(self) -> str:
        """Return the DM output"""
        output = self.game.output()
        logger.info("[DM]: {o}".format(o=output))

        if output:
            prompt = "\n" + output + "\n"
        else:
            prompt = "\n"

        if self.game.state.in_combat:
            prompt += "[COMBAT] "

        prompt += "> "
        if self.game.state.paused:
            prompt += "Press enter to continue... "

        return prompt