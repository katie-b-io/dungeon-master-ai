from dmai.utils.loader import load_json

class MonsterCollection():
    '''MonsterCollection class'''
    
    def __init__(self):
        self.monsters = load_json("data/monsters.json")
    
    def __str__(self):
        monster_list = self.monsters.keys()
        return f"{self.__class__.__name__} is storing the following monsters: \
            {', '.join(monster_list)}"
    
    