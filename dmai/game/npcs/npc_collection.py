from dmai.utils.output_builder import OutputBuilder
from dmai.utils.exceptions import UnrecognisedEntityError
from dmai.domain.monsters.monster_collection import MonsterCollection
from dmai.game.adventure import Adventure
from dmai.game.npcs.npc import NPC
from dmai.domain.monsters.monster import Monster
from dmai.game.state import State, Status
from dmai.utils.config import Config
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class NPCCollection:
    def __init__(self, adventure: Adventure, state: State, output_builder: OutputBuilder) -> None:
        """NPCCollection class"""
        self.adventure = adventure
        self.state = state
        self.output_builder = output_builder

    def load(self) -> None:
        self.npcs = self._create_npcs()
        if Config.no_monsters:
            self.monsters = {}
        else:
            self.monsters = self._create_monsters()

    def __repr__(self) -> str:
        npc_list = self.npcs.keys()
        monster_list = self.monsters.keys()
        npc_str = "{c} is storing the following NPCs: {n}\n{c} is storing the following monsters: {m}".format(
            c=self.__class__.__name__,
            n=", ".join(npc_list),
            m=", ".join(monster_list))
        return npc_str

    def _create_npcs(self) -> None:
        """Method to create all the NPCs"""
        npcs = {}
        for npc_id in self.adventure.npcs:
            npc_data = self.adventure.npcs[npc_id]
            if "monster" not in npc_data:
                npc = NPC(npc_data)
                if npc.id not in self.state.npc_trigger_map:
                    self.state.npc_trigger_map[npc.id] = []
            else:
                npc = MonsterCollection.get_monster_npc(npc_data, self.state, self.output_builder)
            self.state.set_init_npc(npc_data)
            npcs[npc_id] = npc
            # update state with npc location
            for room in self.adventure.rooms:
                if npc_id in self.adventure.rooms[room].npcs:
                    if npc_id not in self.state.current_room:
                        self.state.set_init_room(npc_id, room)
                    break
        return npcs

    def _create_monsters(self) -> None:
        """Method to create all the monsters"""
        monsters = {}
        for room in self.adventure.rooms:
            for monster_id in self.adventure.rooms[room].monsters:
                monster_dict = self.adventure.rooms[room].monsters[monster_id]
                for (status, treasure,
                     must_kill, will_attack_player) in zip(monster_dict["status"],
                                       monster_dict["treasure"],
                                       monster_dict["must_kill"],
                                       monster_dict["will_attack_player"]):
                    # create a monster with unique id
                    i = 1 + sum(
                        1 for m in monsters.values() if m.id == monster_id)
                    unique_id = "{m}_{i}".format(i=i, m=monster_id)
                    monster = MonsterCollection.get_monster(monster_id, self.state, self.output_builder, unique_id=unique_id)
                    monster.set_treasure(treasure)
                    monster.set_must_kill(must_kill)
                    monster.set_will_attack_player(will_attack_player)
                    monsters[unique_id] = monster
                    # initialise self.state
                    self.state.set_init_monster(unique_id, room, status, monster.hp_max)
        return monsters

    def get_type(self, npc_id: str) -> bool:
        """Return str with type of npc"""
        if npc_id in self.npcs:
            return "npc"
        elif npc_id in self.monsters:
            return "monster"

    def get_entity(self, npc_id):
        """Return the Monster/NPC with specified id"""
        try:
            if self.get_type(npc_id) == "npc":
                return self.get_npc(npc_id)
            elif self.get_type(npc_id) == "monster":
                return self.get_monster(npc_id)
            msg = "NPC id not recognised: {e}".format(e=npc_id)
            raise UnrecognisedEntityError(msg)
        except UnrecognisedEntityError:
            raise

    def get_npc(self, npc_id: str) -> NPC:
        """Return NPC with specified id"""
        npc = None
        try:
            npc = self.npcs[npc_id]
        except KeyError as e:
            msg = "NPC id not recognised: {e}".format(e=e)
            raise UnrecognisedEntityError(msg)
        return npc

    def get_monster(self, monster_id: str) -> Monster:
        """Return monster with specified id"""
        monster = None
        try:
            monster = self.monsters[monster_id]
        except KeyError as e:
            msg = "Monster id not recognised: {e}".format(e=e)
            raise UnrecognisedEntityError(msg)
        return monster

    def get_monster_id(self,
                       monster_type: str,
                       status: str = None,
                       location: str = None) -> None:
        """Method to find a monster of specified type and status.
        Returns a string with the monster id matching requirements."""
        for monster_id in self.monsters:
            monster = self.monsters[monster_id]
            if monster.id == monster_type:
                try:
                    select = True
                    if status:
                        if Status(status) != self.state.get_current_status(
                                monster_id):
                            select = False
                    if location:
                        if location != self.state.get_current_room_id(monster_id):
                            select = False
                    if select:
                        return monster_id
                except UnrecognisedEntityError as e:
                    logger.error(e)

    def get_all_npcs(self) -> list:
        """Method to return all NPC objects in a list.
        Returns a list of NPCs"""
        return list(self.npcs.values())

    def get_all_npc_ids(self) -> list:
        """Method to return all NPC IDs in a list.
        Returns a list of NPC IDs"""
        return list(self.npcs.keys())

    def get_all_monsters(self) -> list:
        """Method to return all monster objects in a list.
        Returns a list of monsters"""
        return list(self.monsters.values())

    def get_all_monster_ids(self) -> list:
        """Method to return all monster IDs in a list.
        Returns a list of monster IDs"""
        return list(self.monsters.keys())
