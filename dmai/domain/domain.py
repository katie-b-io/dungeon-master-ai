from dmai.domain.monsters import MonsterCollection

class Domain():
    
    # instance variables
    monsters = None
    
    def __init__(self):
        print("I'm the domain")
        
    def load_all(self):
        self.monsters = MonsterCollection()
    
        print(self.monsters)
    
    
    