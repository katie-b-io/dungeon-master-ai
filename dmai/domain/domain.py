from dmai.domain.monsters import MonsterCollection

class Domain():
    
    def __init__(self) -> None:
        '''Domain holds all the information about the world'''
        self.monsters = None
        
    def load_all(self) -> None:
        '''Function to load all the elements of the domain into the
        Domain object'''
        self.monsters = MonsterCollection()
        print(self.monsters)
    