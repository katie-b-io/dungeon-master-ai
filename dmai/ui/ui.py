from dmai.utils.output_builder import OutputBuilder
from dmai.game.game import Game
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class UserInterface:
    def __init__(self, game: Game) -> None:
        """UserInterface class for the game and interacting with the DM"""
        self.game = game
    
    @property
    def output_builder(self) -> OutputBuilder:
        return self.game.output_builder

    def execute(self) -> None:
        """Execute function which allows CLI communication between
        player and DM"""
        while True:
            output = self.game.output()
            logger.info("(SESSION {s}) [DM]: {o}".format(s=self.game.state.session.session_id, o=output.replace("\n", "\\n")))

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
            logger.info("(SESSION {s}) [PLAYER]: {i}".format(s=self.game.state.session.session_id, i=user_input.replace("\n", "\\n")))
            self.game.input(user_input)

    def input(self, user_input: str) -> None:
        """Input the user input"""
        logger.info("(SESSION {s}) [PLAYER]: {i}".format(s=self.game.state.session.session_id, i=user_input.replace("\n", "\\n")))
        self.game.input(user_input)
    
    def output(self) -> str:
        """Return the DM output"""
        output = self.game.output()
        logger.info("(SESSION {s}) [DM]: {o}".format(s=self.game.state.session.session_id, o=output.replace("\n", "\\n")))

        if output:
            prompt = "\n" + output + "\n"
        else:
            prompt = "\n"

        if self.game.state.in_combat:
            prompt += "[COMBAT] "

        prompt += "> "
        if self.game.state.paused:
            prompt += "Press enter to continue... "

        return (prompt, self.game.state.game_ended)

    def save(self) -> dict:
        """Method to save the game state.
        Returns a dict."""
        return self.game.state.save()

    def character_sheet(self) -> str:
        """Method to return the character sheet in a string"""
        return self.game.state.get_player().get_character_sheet()
    
    def players_guide(self) -> str:
        """Method to return the player's guide in a string"""
        return self.game.players_guide