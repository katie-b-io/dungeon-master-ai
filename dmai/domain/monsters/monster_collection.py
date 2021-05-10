from dmai.utils.loader import Loader
from dmai.domain.monsters.monster import Monster
from dmai.domain.monsters.cat import Cat
from dmai.domain.monsters.giant_rat import GiantRat
from dmai.domain.monsters.goblin import Goblin
from dmai.domain.monsters.skeleton import Skeleton
from dmai.domain.monsters.zombie import Zombie


class MonsterCollectionMeta(type):
    _instances = {}

    def __new__(cls, name, bases, dict):
        instance = super().__new__(cls, name, bases, dict)
        instance.monster_data = Loader.load_json("data/monsters.json")
        return instance
    
    def __call__(cls, *args, **kwargs) -> None:
        """MonsterCollection static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
    
class MonsterCollection(metaclass=MonsterCollectionMeta):

    # class variables
    monster_data = dict()

    def __init__(self) -> None:
        """MonsterCollection static class"""
        pass

    def __repr__(self) -> str:
        monster_list = self.monster_data.keys()
        monster_str = "{c} is storing the following monsters: {m}".format(
            c=self.__class__.__name__, m=", ".join(monster_list)
        )
        return monster_str
    
    @classmethod
    def get_monster(cls, monster_id: str) -> Monster:
        """Return a monster of specified type"""
        monster = None
        try:
            monster = cls._monster_factory(monster_id)
            cls.monster_data[monster.name] = monster
        except ValueError as e:
            print(e)
        return monster

    @classmethod
    def _monster_factory(cls, monster: str) -> Monster:
        """Construct a monster of specified type"""
        monster_id = monster.lower()
        if monster_id in cls.monster_data.keys():
            monster_map = {
                "cat": Cat,
                "giant_rat": GiantRat,
                "goblin": Goblin,
                "skeleton": Skeleton,
                "zombie": Zombie,
            }
            monster_obj = monster_map[monster_id]
        else:
            msg = "Cannot create monster_id {m} - it does not exist!".format(m=monster_id)
            raise ValueError(msg)
        return monster_obj(cls.monster_data[monster_id])
