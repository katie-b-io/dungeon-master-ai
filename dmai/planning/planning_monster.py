from abc import ABC, abstractmethod
import os

from dmai.planning.planning_agent import PlanningAgent
from dmai.domain.abilities import Abilities
from dmai.domain.skills import Skills
from dmai.utils.config import Config
from dmai.game.state import State
from dmai.utils.logger import get_logger

logger = get_logger(__name__)


class PlanningMonster(PlanningAgent):
    def __init__(self, state: State, **kwargs) -> None:
        """PlanningMonster class"""
        PlanningAgent.__init__(self, Config.planner.monster, "monster", **kwargs)
        self.state = state

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def build_domain(self) -> None:
        logger.debug("Building domain")
        domain_file = os.path.join(
            Config.directory.planning,
            "{u}.{d}.domain.pddl".format(u=Config.uuid, d=self.domain),
        )

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
                        "ability",
                        "room",
                        "weapon",
                        "armor",
                        "damage_vulnerability",
                        "damage_immunity",
                        "condition_immunity",
                        "language",
                    ],
                }
            )
            types.append({"type": "entity", "subtypes": ["player", "npc", "monster"]})
            types.append({"type": "ability", "subtypes": ["skill"]})
            types.append({"type": "weapon", "subtypes": ["ranged_weapon"]})
            writer.write(self._construct_types(types))

            ################################################
            # Construct the domain file predicates
            predicates = []

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
                    "params": [("monster", "monster"), ("object", "object")],
                }
            )
            predicates.append(
                {"predicate": "higher_than_ac", "params": [("target", "object")]}
            )
            predicates.append(
                {
                    "predicate": "can_attack_roll",
                    "params": [("monster", "monster"), ("target", "object")],
                }
            )
            predicates.append(
                {
                    "predicate": "can_damage_roll",
                    "params": [("monster", "monster"), ("target", "object")],
                }
            )
            predicates.append(
                {
                    "predicate": "can_ability_check",
                    "params": [
                        ("monster", "monster"),
                        ("ability", "ability"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "ability_check_success",
                    "params": [
                        ("monster", "monster"),
                        ("ability", "ability"),
                        ("target", "object"),
                    ],
                }
            )
            predicates.append(
                {
                    "predicate": "attack_roll_success",
                    "params": [("monster", "monster"), ("target", "object")],
                }
            )
            predicates.append({"predicate": "action", "params": []})
            predicates.append({"predicate": "combat", "params": []})
            predicates.append(
                {"predicate": "must_kill", "params": [("player", "player")]}
            )
            predicates.append(
                {
                    "predicate": "attacked",
                    "params": [("entity", "entity"), ("target", "object")],
                }
            )
            predicates.append({"predicate": "torch_lit", "params": []})
            predicates.append({"predicate": "darkvision", "params": []})
            predicates.append({"predicate": "dark", "params": [("room", "room")]})
            writer.write(self._construct_predicates(predicates))

            ################################################
            # Construct the domain file actions
            actions = [
                "ability_check",
                "ability_check_with_advantage",
                "ability_check_with_disadvantage",
                "attack_roll",
                "attack_roll_with_advantage",
                "attack_roll_with_disadvantage",
                "damage_roll",
                "equip",
                "unequip",
                "declare_attack_against_player",
                "kill_player",
            ]
            writer.write(self._construct_actions(actions))
            writer.write(self._construct_domain_footer())

    def build_problem(self) -> None:
        logger.debug("Building problem")
        monster = self.state.get_entity(self.problem)
        problem_file = os.path.join(
            Config.directory.planning,
            "{u}.{p}.problem.pddl".format(u=Config.uuid, p=self.problem),
        )

        with open(problem_file, "w") as writer:
            ################################################
            # Construct the problem file header
            writer.write(self._construct_problem_header(monster.unique_id, "monster"))

            ################################################
            # Construct the problem file objects
            objects = []

            # Player
            objects.append(["player", "player"])

            # Monsters
            objects.append([monster.unique_id, "monster"])

            # Rooms
            objects.append([self.state.get_current_room_id(monster.unique_id), "room"])

            # Weapons
            for attack in monster.get_all_attack_ids():
                objects.append([attack, "weapon"])

            # Construct the string
            writer.write(self._construct_objects(objects))

            ################################################
            # Construct the problem file init
            init = []

            # Player
            init.append(["at", "player", self.state.get_current_room().id])
            if self.state.is_alive():
                init.append(["alive", "player"])

            # Monsters
            init.append(["at", monster.unique_id, self.state.get_current_room(monster.unique_id).id])
            if self.state.is_alive(monster.unique_id):
                init.append(["alive", monster.unique_id])
            if monster.has_darkvision():
                init.append(["darkvision"])
            if not self.state.get_current_room(monster.unique_id).visibility:
                init.append(["dark", self.state.get_current_room(monster.unique_id).id])

            # Weapons
            for attack in monster.get_all_attack_ids():
                init.append(["has", monster.unique_id, attack])
                init.append(["equipped", monster.unique_id, attack])

            # Combat
            if monster.will_attack_player:
                # TODO check if player is visible to monster
                init.append(["must_kill", "player"])
            else:
                for m in self.state.get_possible_monster_targets(monster.unique_id):
                    if self.state.was_attacked(m.unique_id):
                        init.append(["must_kill", "player"])
                        break
            if self.state.was_attacked(monster.unique_id):
                init.append(["attacked", "player", monster.unique_id])

            # Construct the string
            writer.write(self._construct_init(init))

            ################################################
            # Construct the problem file goal
            goal = []
            goal.append(["not", "must_kill", "player"])
            goal.append(["not", "attacked", "player", monster.unique_id])
            alt_goal = []
            alt_goal.append(["not", "alive", "player"])

            writer.write(self._construct_goal(goal, alt_goal=alt_goal))
            writer.write(self._construct_problem_footer())
