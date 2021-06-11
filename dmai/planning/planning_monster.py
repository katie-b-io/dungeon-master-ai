from abc import ABC, abstractmethod
import os

from dmai.planning.planning_agent import PlanningAgent
from dmai.utils.config import Config
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
        logging.debug("Building domain")
        domain_file = os.path.join(
            Config.directory.planning, "{u}.{d}.pddl".format(u=Config.uuid,
                                                             d=self.domain))

        with open(domain_file, 'w') as writer:
            writer.write("""
                ;Dungeons and Dragons 5th Edition Domain

                (define (domain dnd_monster)

                    (:requirements 
                        :strips
                        :action-costs
                        :typing
                        :conditional-effects
                        :negative-preconditions
                        :equality
                    :disjunctive-preconditions)

                    (:types 
                        ; Entities exist
                        entity - object
                        player npc monster - entity
                        ; Monsters exist
                        cat giant_rat goblin skeleton zombie - monster
                        ; Abilities and skills exist
                        ability - object
                        skill - ability
                        ; Rooms exist
                        room - object
                        ; Weapons exist
                        weapon - object
                        ; Ranged weapons exist
                        ranged_weapon
                        ; Armor exists
                        armor - object
                        ; Damage vulnerabilities exist
                        damage_vulnerability - object
                        ; Damage immunities exist
                        damage_immunity - object
                        ; Condition immunities exist
                        condition_immunity - object
                        ; Languages exist
                        language - object
                    )
                    
                    (:predicates 
                        ; Rolls
                        (advantage ?monster - monster ?object - object)
                        (disadvantage ?monster - monster ?object - object)
                        ; Abilities
                        (charisma ?ability - ability)
                        (constitution ?ability - ability)
                        (dexterity ?ability - ability)
                        (intelligence ?ability - ability)
                        (strength ?ability - ability)
                        (wisdom ?ability - ability)
                        ; Skills
                        (acrobatics ?skill - skill)
                        (animal_handling ?skill - skill)
                        (arcana ?skill - skill)
                        (athletics ?skill - skill)
                        (deception ?skill - skill)
                        (history ?skill - skill)
                        (insight ?skill - skill)
                        (intimidation ?skill - skill)
                        (investigation ?skill - skill)
                        (medicine ?skill - skill)
                        (nature ?skill - skill)
                        (perception ?skill - skill)
                        (performance ?skill - skill)
                        (persuasion ?skill - skill)
                        (religion ?skill - skill)
                        (sleight_of_hand ?skill - skill)
                        (stealth ?skill - skill)
                        (survival ?skill - skill)
                        ; Entity has an object
                        (has ?entity - entity ?object - object)
                        ; Object is in a room
                        (at ?object - object ?room - room)
                        ; Object is alive
                        (alive ?object - object)
                        ; Object is damaged
                        (damaged ?object - object)
                        ; Object is equipped by monster
                        (equipped ?monster - monster ?object - object)
                        ; Attack roll exceeds AC of object
                        (higher_than_ac ?target - object)
                        ; Monster can perform an attack roll
                        (can_attack_roll ?monster - monster ?target - object)
                        ; Monster can perform a damage roll
                        (can_damage_roll ?monster - monster ?target - object)
                        ; Monster can perform an ability check
                        (can_ability_check ?monster - monster ?ability - ability ?target - object)
                        ; Monster makes a successful ability check
                        (ability_check_success ?monster - monster ?ability - ability ?target - object)
                        ; Monster makes a successful attack roll against target
                        (attack_roll_success ?monster - monster ?target - object)
                        ; Action is performed
                        (action)
                        ; Combat
                        (combat)
                        (must_kill ?player - player)
                        (attacked ?entity - entity ?target - entity)
                    )

                    ; ================================================================
                    ; Rolls

                    ; Monster succeeds on an ability check
                    (:action ability_check
                        :parameters (?monster - monster ?ability - ability ?target - object ?location - room)
                        :precondition (and 
                            (or
                                (and
                                    (not (advantage ?monster ?ability))
                                    (not (disadvantage ?monster ?ability))
                                )
                                (and
                                    (advantage ?monster ?ability)
                                    (disadvantage ?monster ?ability)
                                )
                            )
                            (at ?monster ?location)
                            (at ?target ?location)
                            (can_ability_check ?monster ?ability ?target)
                            (not (ability_check_success ?monster ?ability ?target))
                        )
                        :effect (and 
                            (not (can_ability_check ?monster ?ability ?target))
                            (ability_check_success ?monster ?ability ?target)
                        )
                    )

                    ; Monster succeeds on an ability check with advantage
                    (:action ability_check_with_advantage
                        :parameters (?monster - monster ?ability - ability ?target - object ?location - room)
                        :precondition (and 
                            (advantage ?monster ?ability)
                            (not (disadvantage ?monster ?ability))
                            (at ?monster ?location)
                            (at ?target ?location)
                            (can_ability_check ?monster ?ability ?target)
                            (not (ability_check_success ?monster ?ability ?target))
                        )
                        :effect (and 
                            (not (can_ability_check ?monster ?ability ?target))
                            (ability_check_success ?monster ?ability ?target)
                        )
                    )

                    ; Monster succeeds on an ability check with disadvantage
                    (:action ability_check_with_disadvantage
                        :parameters (?monster - monster ?ability - ability ?target - object ?location - room)
                        :precondition (and 
                            (not (advantage ?monster ?ability))
                            (disadvantage ?monster ?ability)
                            (at ?monster ?location)
                            (at ?target ?location)
                            (can_ability_check ?monster ?ability ?target)
                            (not (ability_check_success ?monster ?ability ?target))
                        )
                        :effect (and 
                            (not (can_ability_check ?monster ?ability ?target))
                            (ability_check_success ?monster ?ability ?target)
                        )
                    )

                    ; Monster succeeds on an attack roll
                    (:action attack_roll
                        :parameters (?monster - monster ?weapon - weapon ?target - object ?location - room)
                        :precondition (and 
                            (or
                                (and
                                    (not (advantage ?monster ?weapon))
                                    (not (disadvantage ?monster ?weapon))
                                )
                                (and
                                    (advantage ?monster ?weapon)
                                    (disadvantage ?monster ?weapon)
                                )
                            )
                            (at ?monster ?location)
                            (at ?target ?location)
                            (can_attack_roll ?monster ?target)
                            (equipped ?monster ?weapon)
                            (not (attack_roll_success ?monster ?target))
                        )
                        :effect (and 
                            (not (can_attack_roll ?monster ?target))
                            (attack_roll_success ?monster ?target)
                            (higher_than_ac ?target)
                        )
                    )

                    
                    ; Monster succeeds on an attack roll with advantage
                    (:action attack_roll_with_advantage
                        :parameters (?monster - monster ?weapon - weapon ?target - object ?location - room)
                        :precondition (and 
                            (advantage ?monster ?weapon)
                            (not (disadvantage ?monster ?weapon))
                            (at ?monster ?location)
                            (at ?target ?location)
                            (can_attack_roll ?monster ?target)
                            (equipped ?monster ?weapon)
                            (not (attack_roll_success ?monster ?target))
                        )
                        :effect (and 
                            (not (can_attack_roll ?monster ?target))
                            (attack_roll_success ?monster ?target)
                            (higher_than_ac ?target)
                        )
                    )

                    ; Monster succeeds on an attack roll with disadvantage
                    (:action attack_roll_with_disadvantage
                        :parameters (?monster - monster ?weapon - weapon ?target - object ?location - room)
                        :precondition (and 
                            (not (advantage ?monster ?weapon))
                            (disadvantage ?monster ?weapon)
                            (at ?monster ?location)
                            (at ?target ?location)
                            (can_attack_roll ?monster ?target)
                            (equipped ?monster ?weapon)
                            (not (attack_roll_success ?monster ?target))
                        )
                        :effect (and 
                            (not (can_attack_roll ?monster ?target))
                            (attack_roll_success ?monster ?target)
                            (higher_than_ac ?target)
                        )
                    )

                    ; Monster damages a target
                    (:action damage_roll
                        :parameters (?monster - monster ?target - object ?location - room)
                        :precondition (and 
                            (at ?monster ?location)
                            (at ?target ?location)
                            (can_damage_roll ?monster ?target)
                            (alive ?target)
                            (higher_than_ac ?target)
                        )
                        :effect (and 
                            (not (can_damage_roll ?monster ?target))
                            (not (higher_than_ac ?target))
                            (damaged ?target)
                        )
                    )

                    ; ================================================================
                    ; Basic monster actions

                    ; Monster equips weapon or equipment
                    (:action equip
                        :parameters (?monster - monster ?object - object)
                        :precondition (and 
                            (has ?monster ?object)
                            (not (equipped ?monster ?object))
                        )
                        :effect (and 
                            (equipped ?monster ?object)
                        )
                    )
                    
                    ; Monster unequips weapon or equipment
                    (:action unequip
                        :parameters (?monster - monster ?object - object)
                        :precondition (and 
                            (has ?monster ?object)
                            (equipped ?monster ?object)
                        )
                        :effect (and 
                            (not (equipped ?monster ?object))
                        )
                    )

                    ; ================================================================
                    ; Combat

                    ; Monster wants to attack another entity
                    (:action declare_attack_against_entity
                        :parameters (?monster - monster ?target - entity ?location - room)
                        :precondition (and 
                            (alive ?monster)
                            (alive ?target)
                            (at ?monster ?location)
                            (at ?target ?location)
                            (not (action))
                        )
                        :effect (and 
                            (can_attack_roll ?monster ?target)
                            (action)
                        )
                    )

                    ; Monster attacks a target
                    (:action attack_target
                        :parameters (?monster - monster ?weapon - weapon ?target - entity ?location - room)
                        :precondition (and 
                            (action)
                            (alive ?monster)
                            (alive ?target)
                            (at ?monster ?location)
                            (at ?target ?location)
                            (equipped ?monster ?weapon)
                            (attack_roll_success ?monster ?target)
                        )
                        :effect (and 
                            (combat)
                            (can_damage_roll ?monster ?target)
                            (not (attack_roll_success ?monster ?target))
                        )
                    )

                    ; Monster kills a target
                    (:action kill_target
                        :parameters (?monster - monster ?target - entity ?location - room)
                        :precondition (and 
                            (action)
                            (combat)
                            (alive ?monster)
                            (alive ?target)
                            (at ?monster ?location)
                            (at ?target ?location)
                            (damaged ?target)
                        )
                        :effect (and 
                            (not (action))
                            (not (combat))
                            (not (alive ?target))
                        )
                    )

                )
                """)

    def build_problem(self) -> None:
        logging.debug("Building problem")
        problem_file = os.path.join(
            Config.directory.planning, "{u}.{p}.pddl".format(u=Config.uuid,
                                                             p=self.problem))

        with open(problem_file, 'w') as writer:
            writer.write("""
                (define (problem inns_cellar) (:domain dnd_monster)

                (:objects 
                    ; Monsters
                    giant_rat1 - giant_rat
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
                    (alive giant_rat1)
                    (alive giant_rat2)
                    (alive giant_rat3)
                    (alive giant_rat4)
                    (at giant_rat1 inns_cellar)
                    (at giant_rat2 inns_cellar)
                    (at giant_rat3 inns_cellar)
                    (at giant_rat4 inns_cellar)
                    ; set weapons
                    (has giant_rat1 bite)
                    (has giant_rat1 claws)
                    (has giant_rat2 bite)
                    (has giant_rat2 claws)
                    (has giant_rat3 bite)
                    (has giant_rat3 claws)
                    (has giant_rat4 bite)
                    (has giant_rat4 claws)
                    (equipped giant_rat1 bite)
                    (equipped giant_rat1 claws)
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
                    (advantage giant_rat1 bite)
                    (advantage giant_rat1 claws)
                    (advantage giant_rat2 bite)
                    (advantage giant_rat2 claws)
                    (advantage giant_rat3 bite)
                    (advantage giant_rat3 claws)
                    (advantage giant_rat4 bite)
                    (advantage giant_rat4 claws)
                    (attacked player giant_rat1)
                )

                (:goal (and
                    (or 
                        (and
                            (not (attacked player giant_rat1))
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
                """)
