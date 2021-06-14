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
    def __init__(self, **kwargs) -> None:
        """PlanningMonster class"""
        PlanningAgent.__init__(self, Config.planner.monster, "monster",
                               **kwargs)

    def __repr__(self) -> str:
        return "{c}".format(c=self.__class__.__name__)

    def build_domain(self) -> None:
        logger.debug("Building domain")
        domain_file = os.path.join(
            Config.directory.planning, "{u}.{d}.domain.pddl".format(u=Config.uuid,
                                                             d=self.domain))

        with open(domain_file, 'w') as writer:
            ################################################
            # Construct the domain file header and requirements
            writer.write(self._construct_domain_header(self.domain))
            writer.write(self._construct_requirements())

            ################################################
            # Construct the domain file types
            types = []

            # Append types
            types.append({
                "type":
                "object",
                "subtypes": [
                    "entity", "ability", "room", "weapon", "armor",
                    "damage_vulnerability", "damage_immunity",
                    "condition_immunity", "language"
                ]
            })
            types.append({
                "type": "entity",
                "subtypes": ["player", "npc", "monster"]
            })
            types.append({"type": "ability", "subtypes": ["skill"]})
            types.append({"type": "weapon", "subtypes": ["ranged_weapon"]})
            writer.write(self._construct_types(types))

            ################################################
            # Construct the domain file predicates
            predicates = []

            predicates.append({
                "predicate": "advantage",
                "params": [("object", "object")]
            })
            predicates.append({
                "predicate": "disadvantage",
                "params": [("object", "object")]
            })
            for ability in Abilities.get_all_abilities():
                predicates.append({
                    "predicate": ability[1].lower(),
                    "params": [("ability", "ability")]
                })
            for skill in Skills.get_all_skills():
                predicates.append({
                    "predicate": skill[0],
                    "params": [("skill", "skill")]
                })
            predicates.append({
                "predicate":
                "has",
                "params": [("entity", "entity"), ("object", "object")]
            })
            predicates.append({
                "predicate":
                "at",
                "params": [("object", "object"), ("room", "room")]
            })
            predicates.append({
                "predicate": "alive",
                "params": [("object", "object")]
            })
            predicates.append({
                "predicate": "damaged",
                "params": [("object", "object")]
            })
            predicates.append({
                "predicate":
                "equipped",
                "params": [("monster", "monster"), ("object", "object")]
            })
            predicates.append({
                "predicate": "higher_than_ac",
                "params": [("target", "object")]
            })
            predicates.append({
                "predicate":
                "can_attack_roll",
                "params": [("monster", "monster"), ("target", "object")]
            })
            predicates.append({
                "predicate":
                "can_damage_roll",
                "params": [("monster", "monster"), ("target", "object")]
            })
            predicates.append({
                "predicate":
                "can_ability_check",
                "params": [("monster", "monster"), ("ability", "ability"),
                           ("target", "object")]
            })
            predicates.append({
                "predicate":
                "ability_check_success",
                "params": [("monster", "monster"), ("ability", "ability"),
                           ("target", "object")]
            })
            predicates.append({
                "predicate":
                "attack_roll_success",
                "params": [("monster", "monster"), ("target", "object")]
            })
            predicates.append({"predicate": "action", "params": []})
            predicates.append({"predicate": "combat", "params": []})
            predicates.append({
                "predicate": "must_kill",
                "params": [("player", "player")]
            })
            predicates.append({
                "predicate":
                "attacked",
                "params": [("entity", "entity"), ("target", "object")]
            })
            writer.write(self._construct_predicates(predicates))

            ################################################
            # Construct the domain file actions
            actions = [
                "ability_check", "ability_check_with_advantage",
                "ability_check_with_disadvantage", "attack_roll",
                "attack_roll_with_advantage", "attack_roll_with_disadvantage",
                "damage_roll", "equip", "unequip",
                "declare_attack_against_entity", "attack_player", "kill_player"
            ]
            writer.write(self._construct_actions(actions))
            writer.write(self._construct_domain_footer())

    def build_problem(self) -> None:
        logger.debug("Building problem")
        problem_file = os.path.join(
            Config.directory.planning, "{u}.{p}.problem.pddl".format(u=Config.uuid,
                                                             p=self.problem))

        with open(problem_file, 'w') as writer:
            ################################################
            # Construct the problem file header
            writer.write(
                self._construct_problem_header(self.problem, "monster"))

            ################################################
            # Construct the problem file objects
            objects = []

            # Player
            objects.append(("player", "player"))

            # Monsters
            objects.append(("giant_rat_1", "monster"))

            # Room
            objects.append(("inns_cellar", "room"))

            # Weapons
            objects.append(("bite", "weapon"))
            objects.append(("claws", "weapon"))

            # Construct the string
            writer.write(self._construct_objects(objects))

            ################################################
            # Construct the problem file init
            init = []

            # Player
            init.append(("at", "player", State.get_current_room().id))
            if State.is_alive():
                init.append(("alive", "player"))

            # Monsters
            init.append(("at", "giant_rat_1", State.get_current_room("giant_rat_1").id))
            if State.is_alive("giant_rat_1"):
                init.append(("alive", "giant_rat_1"))

            # TODO create these statements automatically
            # Weapons
            init.append(("has", "giant_rat_1", "bite"))
            init.append(("has", "giant_rat_1", "claws"))
            init.append(("equipped", "giant_rat_1", "bite"))
            init.append(("equipped", "giant_rat_1", "claws"))

            # Combat
            init.append(("must_kill", "player"))

            # Construct the string
            writer.write(self._construct_init(init))

            ################################################
            # Construct the problem file goal
            goal = []
            goal.append(("not", "attacked", "player", "giant_rat_1"))
            alt_goal = []
            alt_goal.append(("not", "alive", "player"))

            writer.write(self._construct_goal(goal, alt_goal=alt_goal))
            writer.write(self._construct_problem_footer())

            """
                (define (problem inns_cellar) (:domain monster)

                (:objects 
                    ; Monsters
                    giant_rat_1 - giant_rat
                    giant_rat2 - giant_rat
                    giant_rat3 - giant_rat
                    giant_rat4 - giant_rat
                    ; Player
                    player - player
                    ; Room
                    inns_cellar - room
                    ; Weapons
                    bite - weapon
                    claws - weapon
                )

                (:init
                    ; =======================================
                    ; Monster
                    (alive giant_rat_1)
                    (alive giant_rat2)
                    (alive giant_rat3)
                    (alive giant_rat4)
                    (at giant_rat_1 inns_cellar)
                    (at giant_rat2 inns_cellar)
                    (at giant_rat3 inns_cellar)
                    (at giant_rat4 inns_cellar)
                    ; set weapons
                    (has giant_rat_1 bite)
                    (has giant_rat_1 claws)
                    (has giant_rat2 bite)
                    (has giant_rat2 claws)
                    (has giant_rat3 bite)
                    (has giant_rat3 claws)
                    (has giant_rat4 bite)
                    (has giant_rat4 claws)
                    (equipped giant_rat_1 bite)
                    (equipped giant_rat_1 claws)
                    (equipped giant_rat2 bite)
                    (equipped giant_rat2 claws)
                    (equipped giant_rat3 bite)
                    (equipped giant_rat3 claws)
                    (equipped giant_rat4 bite)
                    (equipped giant_rat4 claws)

                    ; =======================================
                    ; Player
                    (alive player)
                    (at player inns_cellar)

                    ; =======================================
                    ; Combat
                    (must_kill player)
                    (advantage giant_rat_1 bite)
                    (advantage giant_rat_1 claws)
                    (advantage giant_rat2 bite)
                    (advantage giant_rat2 claws)
                    (advantage giant_rat3 bite)
                    (advantage giant_rat3 claws)
                    (advantage giant_rat4 bite)
                    (advantage giant_rat4 claws)
                    (attacked player giant_rat_1)
                )

                (:goal (and
                    (or 
                        (and
                            (not (attacked player giant_rat_1))
                            (not (attacked player giant_rat2))
                            (not (attacked player giant_rat3))
                            (not (attacked player giant_rat4))
                        )
                        (and
                            (not (alive player))
                        )
                    )
                ))

                )
                """
