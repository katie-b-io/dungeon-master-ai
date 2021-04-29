from dmai.domain import Domain

class DM():
    '''Main DM class'''
    
    # instance variables
    domain = None
    player_utter = None
    dm_utter = None
    
    def __init__(self):
        self.dm_utter = "what do you do? "
        
    def load(self):
        '''Load the data'''
        self.domain = Domain()
        self.domain.load_all()
    
    def input(self, player_utter: str):
        '''Receive an input to the DM'''
        self.player_utter = player_utter
        self._generate_utterance()
        
    @property
    def output(self):
        '''Return an output for the player'''
        return self.dm_utter
        
    def _generate_utterance(self):
        '''Generate an utterance for the player'''
        if self.player_utter:
            self.dm_utter = f"{self.player_utter} - are you sure? "
        else:
            self.dm_utter = "what do you do? "