from dmai.dm import DM

class UserInterface():
    '''UserInterface class for interacting with the DM'''
    
    # instance variables
    dm = None
    
    def __init__(self, dm: DM):
        self.dm = dm
        
    def execute(self):
        '''Execute function which allows communication between player and DM'''
        while True:
            prompt = self.dm.output
            user_input = input(prompt)
            self.dm.input(user_input)