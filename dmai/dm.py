from dmai.nlg import NLG

class DM():
    
    def __init__(self) -> None:
        '''Main DM class'''
        self.dm_utter = None
        self.player_utter = None
    
    def input(self, player_utter: str) -> None:
        '''Receive a player input'''
        self.player_utter = player_utter
        self._generate_utterance()
        
    @property
    def output(self) -> str:
        '''Return an output for the player'''
        return self.dm_utter
        
    def _generate_utterance(self) -> str:
        '''Generate an utterance for the player'''
        if self.player_utter:
            self.dm_utter = f"{self.player_utter} - are you sure? "
        else:
            self.dm_utter = NLG.get_action()