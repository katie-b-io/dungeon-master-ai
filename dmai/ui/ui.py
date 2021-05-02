from dmai.game import Game

class UserInterface():
    
    def __init__(self, game: Game) -> None:
        '''UserInterface class for the game and interacting with the DM'''
        self.game = game
        
    def execute(self) -> None:
        '''Execute function which allows CLI communication between
        player and DM'''        
        while True:
            prompt = self.game.output()
            user_input = input(prompt)
            self.game.input(user_input)