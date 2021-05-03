from dmai.utils import Loader
from dmai.domain.monsters import Monster, Cat, GiantRat, Goblin, Skeleton, Zombie

class MonsterCollection():
    
    # class variables
    monster_data = dict()
    
    def __init__(self) -> None:
        '''MonsterCollection class'''
        self._load_monster_data()
        self.monsters = dict()
    
    def __repr__(self) -> str:
        monster_list = self.monsters.keys()
        monster_str = "{c} is storing the following monsters: {m}".format(
            c=self.__class__.__name__,
            m=', '.join(monster_list))
        return monster_str
    
    @classmethod
    def _load_monster_data(self) -> None:
        '''Set the self.monster_data class variable data'''
        self.monster_data = Loader.load_json("data/monsters.json")
        
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
