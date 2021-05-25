from dmai.game.npcs.npc import NPC
from dmai.utils.loader import Loader
from dmai.domain.monsters.monster import Monster
from dmai.domain.monsters.cat import Cat
from dmai.domain.monsters.giant_rat import GiantRat
from dmai.domain.monsters.goblin import Goblin
from dmai.domain.monsters.skeleton import Skeleton
from dmai.domain.monsters.zombie import Zombie
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class MonsterCollectionMeta(type):
    _instances = {}

    def __new__(cls, name, bases, dict):
        instance = super().__new__(cls, name, bases, dict)
        instance.monster_data = Loader.load_domain("monsters")
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
    monster_map = {
        "cat": Cat,
        "giant_rat": GiantRat,
        "goblin": Goblin,
        "skeleton": Skeleton,
        "zombie": Zombie,
    }

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
    def get_monster(cls, monster_cls: str) -> Monster:
        """Return an instance of a monster of specified type"""
        try:
            return cls._monster_factory(monster_cls = monster_cls)
        except ValueError as e:
            logger.error(e)
    
    @classmethod
    def get_monster_npc(cls, npc_data: dict) -> NPC:
        """Return an instance of a monster of specified NPC."""
        try:
            return cls._monster_factory(npc_data = npc_data)
        except ValueError as e:
            logger.error(e)
    
    @classmethod
    def _monster_factory(cls, monster_cls: str = None, npc_data: dict = None) -> Monster:
        """Construct a monster of specified type"""
        try:
            if monster_cls:
                monster_cls = monster_cls.lower()
            else:
                monster_cls = npc_data["monster"].lower()
                
            monster = cls.monster_map[monster_cls]
            return monster(cls.monster_data[monster_cls], npc_data)
        except (ValueError, KeyError) as e:
            msg = "Cannot create monster {m} - it does not exist!".format(m=monster_cls)
            raise ValueError(msg)

