from dmai.utils.loader import load_json
from .monster import Monster
from .cat import Cat
from .giant_rat import GiantRat
from .goblin import Goblin
from .skeleton import Skeleton
from .zombie import Zombie

class MonsterCollection():
    
    # class variables
    monster_data = dict()
    
    def __init__(self) -> None:
        '''MonsterCollection class'''
        self.set_monster_data(load_json("data/monsters.json"))
        self.monsters = dict()
    
    def __str__(self) -> str:
        monster_list = self.monsters.keys()
        monster_str = "{c} is storing the following monsters: {m}".format(
            c=self.__class__.__name__,
            m=', '.join(monster_list))
        return monster_str
    
    @classmethod
    def set_monster_data(self, data: dict) -> None:
        '''Set the self.monster_data class variable data'''
        self.monster_data = data
        
    def get_monster(self, monster: str) -> Monster:
        '''Return a monster of specified type'''
        monster_obj = None
        try:
            monster_obj = self._monster_factory(monster)
            self.monsters[monster_obj.name] = monster_obj
        except ValueError as e:
            print(e)
        return monster_obj
        
    def _monster_factory(self, monster: str) -> Monster:
        '''Construct a monster of specified type'''
        monster = monster.lower()
        if monster in self.monster_data.keys():
            monster_map = {
                'cat': Cat,
                'giant_rat': GiantRat,
                'goblin': Goblin,
                'skeleton': Skeleton,
                'zombie': Zombie
                }
            monster_obj = monster_map[monster]
        else:
            msg = "Cannot construct monster {m} - it does not exist!".format(
                m=monster)
            raise ValueError(msg)
        return monster_obj(self.monster_data[monster])
