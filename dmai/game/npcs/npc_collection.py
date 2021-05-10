from dmai.domain.monsters.monster_collection import MonsterCollection
from dmai.game.adventure import Adventure
from dmai.game.npcs.npc import NPC
from dmai.game.state import State


class NPCCollection:
    def __init__(self, adventure: Adventure) -> None:
        """NPCCollection class"""
        self.adventure = adventure
        self.npcs = self._create_npcs()
        self.monsters = self._create_monsters()

    def __repr__(self) -> str:
        npc_list = self.npcs.keys()
        monster_list = self.monsters.keys()
        npc_str = "{c} is storing the following NPCs: {n}\n{c} is storing the following monsters: {m}".format(
            c=self.__class__.__name__, n=", ".join(npc_list), m=", ".join(monster_list)
        )
        return npc_str

    def _create_npcs(self) -> None:
        """Method to create all the NPCs"""
        npcs = {}
        for npc_id in self.adventure.npcs:
            npc_data = self.adventure.npcs[npc_id]
            if "monster" not in npc_data:
                npc = NPC(npc_data)
            else:
                npc = MonsterCollection.get_monster_npc(npc_data)
            npcs[npc_id] = npc
            # update state with npc location
            for room in self.adventure.rooms:
                if npc_id in self.adventure.rooms[room].npcs:
                    State.set_init_room(npc_id, room)
                    break
        return npcs

    def _create_monsters(self) -> None:
        """Method to create all the monsters"""
        monsters = {}
        for room in self.adventure.rooms:
            for monster_id in self.adventure.rooms[room].monsters:
                monster_dict = self.adventure.rooms[room].monsters[monster_id]
                for (status, treasure) in zip(monster_dict["status"], monster_dict["treasure"]):
                    # create a monster with unique id
                    monster = MonsterCollection.get_monster(monster_id)
                    monster.set_treasure(treasure)
                    unique_id = "{i}_{m}".format(i=len(monsters), m=monster_id)
                    monsters[unique_id] = monster
                    # update state with monster location and status
                    State.set_init_room(unique_id, room)
                    State.set_init_status(unique_id, status)
        return monsters

    def get_npc(self, npc_id: str) -> NPC:
        """Return NPC with specified id"""
        npc = None
        try:
            npc = self.npcs[npc_id]
        except KeyError as e:
            msg = "NPC id not recognised: {e}".format(e=e)
            raise KeyError(msg)
        return npc

    def set_monsters(self, monster_dict: dict) -> None:
        for monster_type in monster_dict:
            for i in range(len(monster_dict[monster_type])):
                monster = self.get_monster(monster_type)
                monster_id = "monster_{i}".format(i=i)
                self.monsters[monster_id] = monster
