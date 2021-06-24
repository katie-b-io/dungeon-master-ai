from abc import ABC, abstractmethod
import os

from dmai.planning.planning_agent import PlanningAgent
from dmai.domain.abilities import Abilities
from dmai.domain.monsters.monster_collection import MonsterCollection
from dmai.domain.skills import Skills
from dmai.utils.config import Config
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class PlanningPlayer(PlanningAgent):
    def __init__(self, **kwargs) -> None:
        """PlanningPlayer class"""
        PlanningAgent.__init__(self, Config.planner.player, "player", **kwargs)

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def build_domain(self) -> None:
        logger.debug("Building domain")
        domain_file = os.path.join(
            Config.directory.planning,
            "{u}.{d}.domain.pddl".format(u=Config.uuid, d=self.domain),
        )

        # TODO implement intent solution
        # TODO implement item solution
        # TODO implement solve intent

        with open(domain_file, "w") as writer:
            ################################################
            # Construct the domain file header and requirements
            writer.write(self._construct_domain_header(self.domain))
            writer.write(self._construct_requirements())

            ################################################
            # Construct the domain file types
            types = []

            # Append types
            types.append(
                {
                    "type": "object",
                    "subtypes": [
                        "entity",
                        "intent",
                        "item",
                        "puzzle",
                        "attitude",
                        "ability",
                        "room",
                        "door",
                        "weapon",
                        "armor",
                        "equipment",
                        "damage_vulnerability",
                        "damage_immunity",
                        "condition_immunity",
                        "language",
                    ],
                }
            )
            types.append({"type": "entity", "subtypes": ["player", "npc", "monster"]})
            types.append(
                {"type": "monster", "subtypes": MonsterCollection.get_all_monsters()}
            )
            types.append(
                {"type": "attitude", "subtypes": ["indifferent", "friendly", "hostile"]}
            )
            types.append({"type": "ability", "subtypes": ["skill"]})
            types.append({"type": "weapon", "subtypes": ["ranged_weapon"]})
            writer.write(self._construct_types(types))

            ################################################
            # Construct the domain file predicates
            predicates = []

            # Adventure
            predicates.append({"predicate": "quest", "params": []})
            predicates.append({"predicate": "complete", "params": []})
            predicates.append({"predicate": "gives_quest", "params": [("npc", "npc")]})
            predicates.append(
                {"predicate": "advantage", "params": [("object", "object")]}
            )
            predicates.append(
                {"predicate": "disadvantage", "params": [("object", "object")]}
            )
            for ability in Abilities.get_all_abilities():
                predicates.append(
                    {
                        "predicate": ability[1].lower(),
                        "params": [("ability", "ability")],
                    }
                )
            for skill in Skills.get_all_skills():
                predicates.append(
                    {"predicate": skill[0], "params": [("skill", "skill")]}
                )
            predicates.append(
                {
                    "predicate": "has",
                    "params": [("entity", "entity"), ("object", "object")],
                }
            )
            predicates.append(
                {"predicate": "at", "params": [("object", "object"), ("room", "room")]}
            )
            predicates.append({"predicate": "alive", "params": [("object", "object")]})
            predicates.append(
                {"predicate": "damaged", "params": [("object", "object")]}
            )
            predicates.append(
                {
                    "predicate": "equipped",
                    "params": [("player", "player"), ("object", "object")],
                }
            )
            predicates.append(
                {
                    "predicate": "connected",
                    "params": [
                        ("door", "door"),
                        ("location", "room"),
                        ("destination", "room"),
                    ],
                }
            )
            predicates.append({"predicate": "locked", "params": [("door", "door")]})
            predicates.append(
                {"predicate": "higher_than_ac", "params": [("target", "object")]}
            )
            predicates.append(
                {
                    "predicate": "can_attack_roll",
                    "params": [("player", "player"), ("target", "object")],
                }
            )
            predicates.append(
                {
                    "predicate": "can_damage_roll",
                    "params": [("player", "player"), ("target", "object")],
                }
            )
            predicates.append(
                {
                    "predicate": "can_ability_check",
                    "params": [
                        ("player", "player"),
                        ("ability", "ability"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "can_equipment_check",
                    "params": [
                        ("player", "player"),
                        ("equipment", "equipment"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "ability_check_success",
                    "params": [
                        ("player", "player"),
                        ("ability", "ability"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "equipment_check_success",
                    "params": [
                        ("player", "player"),
                        ("equipment", "equipment"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "attack_roll_success",
                    "params": [("player", "player"), ("target", "object")],
                }
            )
            for equipment in State.get_player().get_all_equipment_ids():
                predicates.append(
                    {"predicate": equipment, "params": [("equipment", "equipment")]}
                )
            predicates.append({"predicate": "action", "params": []})
            predicates.append(
                {
                    "predicate": "attitude_towards_player",
                    "params": [("npc", "npc"), ("attitude", "attitude")],
                }
            )
            predicates.append(
                {
                    "predicate": "improve_attitude",
                    "params": [("current", "attitude"), ("next", "attitude")],
                }
            )
            predicates.append(
                {
                    "predicate": "degrade_attitude",
                    "params": [("current", "attitude"), ("next", "attitude")],
                }
            )
            predicates.append({"predicate": "combat", "params": []})
            predicates.append(
                {"predicate": "must_kill", "params": [("monster", "monster")]}
            )
            predicates.append(
                {
                    "predicate": "ability_solution",
                    "params": [("target", "object"), ("ability", "ability")],
                }
            )
            predicates.append(
                {
                    "predicate": "equipment_solution",
                    "params": [("target", "object"), ("equipment", "equipment")],
                }
            )
            predicates.append(
                {
                    "predicate": "intent_solution",
                    "params": [("target", "object"), ("intent", "intent")],
                }
            )
            predicates.append(
                {
                    "predicate": "item_solution",
                    "params": [("target", "object"), ("item", "item")],
                }
            )
            writer.write(self._construct_predicates(predicates))

            ################################################
            # Construct the domain file actions
            actions = [
                "ability_check",
                "ability_check_with_advantage",
                "ability_check_with_disadvantage",
                "equipment_check",
                "equipment_check_with_advantage",
                "equipment_check_with_disadvantage",
                "attack_roll",
                "attack_roll_with_advantage",
                "attack_roll_with_disadvantage",
                "damage_roll",
                "equip",
                "unequip",
                "move",
                "open_door_with_ability",
                "open_door_with_equipment",
                "open_door_with_attack",
                "force_door",
                "use_door_switch",
                "attack_door",
                "breaks_down_door",
                "receive_quest",
                "roleplay_positively",
                "roleplay_negatively",
                "declare_attack_against_entity",
                "kill_monster",
            ]
            if State.get_player().has_equipment("thieves_tools")[0]:
                actions.append("use_thieves_tools")
            writer.write(self._construct_actions(actions))
            writer.write(self._construct_domain_footer())

    def build_problem(self) -> None:
        logger.debug("Building problem")
        problem_file = os.path.join(
            Config.directory.planning,
            "{u}.{p}.problem.pddl".format(u=Config.uuid, p=self.problem),
        )

        with open(problem_file, "w") as writer:
            ################################################
            # Construct the problem file header
            writer.write(self._construct_problem_header(self.problem, "player"))

            ################################################
            # Construct the problem file objects
            objects = []

            # Player
            objects.append(["player", "player"])
            for intent in State.get_dm().player_intent_map.keys():
                objects.append([intent, "intent"])
            for item in State.get_all_item_ids():
                objects.append([item, "item"])

            # NPCs
            for npc in State.get_dm().npcs.get_all_npcs():
                objects.append([npc.id, "npc"])
            objects.append(["indifferent", "indifferent"])
            objects.append(["friendly", "friendly"])
            objects.append(["hostile", "hostile"])

            # Rooms
            for room in State.get_dm().adventure.get_all_rooms():
                objects.append([room.id, "room"])

            # Doors
            doors = []
            for room in State.get_dm().adventure.get_all_rooms():
                for connection in room.get_connected_rooms():
                    door = "{r}---{c}".format(r=room.id, c=connection)
                    reverse_door = "{c}---{r}".format(r=room.id, c=connection)
                    if not reverse_door in doors:
                        doors.append(door)
            for door in doors:
                objects.append([door, "door"])

            # Monsters
            for monster in State.get_dm().npcs.get_all_monsters():
                objects.append([monster.unique_id, monster.id])

            # Abilities
            for ability in Abilities.get_all_abilities():
                objects.append([ability[0], "ability"])

            # Skills
            for skill in Skills.get_all_skills():
                objects.append([skill[0], "skill"])

            # Weapons
            for weapon in State.get_player().get_all_weapon_ids():
                objects.append([weapon, "weapon"])

            # Equipment
            for equipment in State.get_player().get_all_equipment_ids():
                objects.append([equipment, "equipment"])

            # Puzzles
            for room in State.get_dm().adventure.get_all_rooms():
                for puzzle in room.puzzles.get_all_puzzles():
                    if not puzzle.type == "door":
                        objects.append([puzzle.id, "puzzle"])

            # Construct the string
            writer.write(self._construct_objects(objects))

            ################################################
            # Construct the problem file init
            init = []

            # Adventure
            if State.questing:
                init.append(["quest"])

            # Player
            init.append(["at", "player", State.get_current_room().id])
            if State.is_alive():
                init.append(["alive", "player"])
            for ability in Abilities.get_all_abilities():
                init.append([ability[1].lower(), ability[0]])
            for skill in Skills.get_all_skills():
                init.append([skill[0], skill[0]])
            for weapon in State.get_player().get_all_weapon_ids():
                init.append(["has", "player", weapon])
                if State.get_player().is_equipped(weapon):
                    init.append(["equipped", "player", weapon])
            for equipment in State.get_player().get_all_equipment_ids():
                init.append([equipment, equipment])
                init.append(["has", "player", equipment])

            # NPCs
            for npc in State.get_dm().npcs.get_all_npcs():
                init.append(["at", npc.id, State.get_current_room(npc.id).id])
                if State.is_alive(npc.id):
                    init.append(["alive", npc.id])
                if npc.gives_quest:
                    init.append(["gives_quest", npc.id])
            init.append(["improve_attitude", "indifferent", "friendly"])
            init.append(["improve_attitude", "hostile", "indifferent"])
            init.append(["degrade_attitude", "friendly", "indifferent"])
            init.append(["degrade_attitude", "indifferent", "hostile"])
            for npc in State.get_dm().npcs.get_all_npcs():
                init.append(
                    [
                        "attitude_towards_player",
                        npc.id,
                        State.get_current_attitude(npc.id).value,
                    ]
                )

            # Monsters
            for monster in State.get_dm().npcs.get_all_monsters():
                init.append(
                    [
                        "at",
                        monster.unique_id,
                        State.get_current_room(monster.unique_id).id,
                    ]
                )
            for monster in State.get_dm().npcs.get_all_monsters():
                if State.is_alive(monster.unique_id):
                    init.append(["alive", monster.unique_id])

            # Combat
            for npc in State.get_dm().npcs.get_all_npcs():
                if npc.must_kill:
                    init.append(["must_kill", npc.id])
            for monster in State.get_dm().npcs.get_all_monsters():
                if monster.must_kill:
                    init.append(["must_kill", monster.unique_id])

            # Rooms
            for door in doors:
                room1 = door.split("---")[0]
                room2 = door.split("---")[1]
                init.append(["connected", door, room1, room2])
                init.append(["connected", door, room2, room1])
                init.append(["at", door, room1])
                init.append(["at", door, room2])
                if not State.travel_allowed(room1, room2):
                    init.append(["locked", door])
                if not State.connection_broken(room1, room2):
                    init.append(["alive", door])

            # Puzzles
            for room in State.get_dm().adventure.get_all_rooms():
                for puzzle in room.puzzles.get_all_puzzles():
                    # Ability solution
                    for ability in Abilities.get_all_abilities():
                        if puzzle.check_solution_ability(ability[0]):
                            init.append(["ability_solution", puzzle.id, ability[0]])
                    # Skill solution
                    for skill in Skills.get_all_skills():
                        if puzzle.check_solution_skill(skill[0]):
                            init.append(["ability_solution", puzzle.id, skill[0]])
                    # Equipment solution
                    for equipment in State.get_player().get_all_equipment_ids():
                        if puzzle.check_solution_equipment(equipment):
                            init.append(["equipment_solution", puzzle.id, equipment])
                    # Intent solution
                    for intent in State.get_dm().player_intent_map.keys():
                        if puzzle.check_solution_intent(intent):
                            init.append(["intent_solution", puzzle.id, intent])
                    # Item solution
                    for item in State.get_all_item_ids():
                        if puzzle.check_solution_item(item):
                            init.append(["item_solution", puzzle.id, item])

                    # TODO add spell solution

            # Construct the string
            writer.write(self._construct_init(init))

            ################################################
            # Construct the problem file goal
            goal = []
            goal.append(State.current_goal)
            writer.write(self._construct_goal(goal))
            writer.write(self._construct_problem_footer())
