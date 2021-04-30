from dmai import DM

class UserInterface():
    
    def __init__(self, dm: DM) -> None:
        '''UserInterface class for interacting with the DM'''
        self.dm = dm
        
    def execute(self) -> None:
        '''Execute function which allows CLI communication between
        player and DM'''
        while True:
            prompt = self.dm.output
            user_input = input(prompt)
            self.dm.input(user_input)