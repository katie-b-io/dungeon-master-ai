from abc import ABC, abstractmethod
import os

from dmai.planning.planning_agent import PlanningAgent
from dmai.domain.abilities import Abilities
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
            "{u}.{d}.domain.pddl".format(u=Config.uuid, d=self.domain))

        # TODO implement intent solution
        # TODO implement item solution
        # TODO implement solve intent

        with open(domain_file, 'w') as writer:
            writer.write("""
;Dungeons and Dragons 5th Edition Domain

(define (domain {d})

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
        ; Intents exist
        intent - object
        ; Items exist
        item - object
        ; Puzzles exist
        puzzle - object
        ; Roleplaying exists
        attitude - object
        indifferent friendly hostile - attitude
        ; Monsters exist
        cat giant_rat goblin skeleton zombie - monster
        ; Monster variants exist
        diseased_giant_rat - giant_rat
        ; Abilities and skills exist
        ability - object
        skill - ability
        ; Rooms exist
        room - object
        ; Doors exist
        door - object
        ; Weapons exist
        weapon - object
        ; Ranged weapons exist
        ranged_weapon
        ; Armor exists
        armor - object
        ; Equipment exists
        equipment - object
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
        ; Adventure
        (quest) ; player has received quest
        (dwarven_thrower) ; player has found dwarven thrower treasure
        (gives_quest ?npc - npc) ; NPC can give quest
        (silver_key) ; player has the silver key
        ; Rolls
        (advantage ?object - object)
        (disadvantage ?object - object)
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
        ; Object is equipped by player
        (equipped ?player - player ?object - object)
        ; Rooms are connected
        (connected ?door - door ?location - room ?destination - room)
        ; Door is locked
        (locked ?door - door)
        ; Attack roll exceeds AC of object
        (higher_than_ac ?target - object)
        ; Player can perform an attack roll
        (can_attack_roll ?player - player ?target - object)
        ; Player can perform a damage roll
        (can_damage_roll ?player - player ?target - object)
        ; Player can perform an ability check
        (can_ability_check ?player - player ?ability - ability ?target - object)
        ; Player can perform an equipment check
        (can_equipment_check ?player - player ?equipment - equipment ?target - object)
        ; Player makes a successful ability check
        (ability_check_success ?player - player ?ability - ability ?target - object)
        ; Player makes a successful equipment check
        (equipment_check_success ?player - player ?equipment - equipment)
        ; Player makes a successful attack roll against target
        (attack_roll_success ?player - player ?target - object)
        ; Equipment
        (arrows ?equipment - equipment)
        (backpack ?equipment - equipment)
        (bedroll ?equipment - equipment)
        (bolts ?equipment - equipment)
        (mess_kit ?equipment - equipment)
        (quiver ?equipment - equipment)
        (rations ?equipment - equipment)
        (rope_hempen ?equipment - equipment)
        (set_of_common_clothes ?equipment - equipment)
        (thieves_tools ?equipment - equipment)
        (tinder_box ?equipment - equipment)
        (torch ?equipment - equipment)
        (waterskin ?equipment - equipment)
        ; Action is performed
        (action)
        ; NPC attitudes
        (attitude_towards_player ?npc - npc ?attitude - attitude)
        (improve_attitude ?current - attitude ?next - attitude)
        (degrade_attitude ?current - attitude ?next - attitude)
        ; Combat
        (combat)
        (must_kill ?monster - monster)
        ; Puzzles
        (dc ?target - object ?ability - ability)
        (dc_equipment ?target - object ?equipment - equipment)
        (intent_solution ?target - object ?intent - intent)
        (item_solution ?target - object ?item - item)
    )

    ; ================================================================
    ; Rolls

    ; Player succeeds on an ability check
    (:action ability_check
        :parameters (?player - player ?ability - ability ?target - object ?location - room)
        :precondition (and 
            (or
                (and
                    (not (advantage ?ability))
                    (not (disadvantage ?ability))
                )
                (and
                    (advantage ?ability)
                    (disadvantage ?ability)
                )
            )
            (at ?player ?location)
            (at ?target ?location)
            (can_ability_check ?player ?ability ?target)
            (not (ability_check_success ?player ?ability ?target))
        )
        :effect (and 
            (not (can_ability_check ?player ?ability ?target))
            (ability_check_success ?player ?ability ?target)
        )
    )

    ; Player succeeds on an ability check with advantage
    (:action ability_check_with_advantage
        :parameters (?player - player ?ability - ability ?target - object ?location - room)
        :precondition (and 
            (advantage ?ability)
            (not (disadvantage ?ability))
            (at ?player ?location)
            (at ?target ?location)
            (can_ability_check ?player ?ability ?target)
            (not (ability_check_success ?player ?ability ?target))
        )
        :effect (and 
            (not (can_ability_check ?player ?ability ?target))
            (ability_check_success ?player ?ability ?target)
        )
    )
    
    ; Player succeeds on an ability check with disadvantage
    (:action ability_check_with_disadvantage
        :parameters (?player - player ?ability - ability ?target - object ?location - room)
        :precondition (and 
            (not (advantage ?ability))
            (disadvantage ?ability)
            (at ?player ?location)
            (at ?target ?location)
            (can_ability_check ?player ?ability ?target)
            (not (ability_check_success ?player ?ability ?target))
        )
        :effect (and 
            (not (can_ability_check ?player ?ability ?target))
            (ability_check_success ?player ?ability ?target)
        )
    )

    ; Player succeeds on an equipment check
    (:action equipment_check
        :parameters (?player - player ?equipment - equipment ?target - object ?location - room)
        :precondition (and 
            (or
                (and
                    (not (advantage ?equipment))
                    (not (disadvantage ?equipment))
                )
                (and
                    (advantage ?equipment)
                    (disadvantage ?equipment)
                )
            )
            (at ?player ?location)
            (at ?target ?location)
            (can_equipment_check ?player ?equipment ?target)
            (not (equipment_check_success ?player ?equipment))
        )
        :effect (and 
            (not (can_equipment_check ?player ?equipment ?target))
            (equipment_check_success ?player ?equipment)
        )
    )

    ; Player succeeds on an equipment check with advantage
    (:action equipment_check_with_advantage
        :parameters (?player - player ?equipment - equipment ?target - object ?location - room)
        :precondition (and 
            (advantage ?equipment)
            (not (disadvantage ?equipment))
            (at ?player ?location)
            (at ?target ?location)
            (can_equipment_check ?player ?equipment ?target)
            (not (equipment_check_success ?player ?equipment))
        )
        :effect (and 
            (not (can_equipment_check ?player ?equipment ?target))
            (equipment_check_success ?player ?equipment)
        )
    )

    ; Player succeeds on an equipment check with disadvantage
    (:action equipment_check_with_disadvantage
        :parameters (?player - player ?equipment - equipment ?target - object ?location - room)
        :precondition (and 
            (not (advantage ?equipment))
            (disadvantage ?equipment)
            (at ?player ?location)
            (at ?target ?location)
            (can_equipment_check ?player ?equipment ?target)
            (not (equipment_check_success ?player ?equipment))
        )
        :effect (and 
            (not (can_equipment_check ?player ?equipment ?target))
            (equipment_check_success ?player ?equipment)
        )
    )

    ; Player succeeds on an attack roll
    (:action attack_roll
        :parameters (?player - player ?weapon - weapon ?target - object ?location - room)
        :precondition (and 
            (or
                (and
                    (not (advantage ?weapon))
                    (not (disadvantage ?weapon))
                )
                (and
                    (advantage ?weapon)
                    (disadvantage ?weapon)
                )
            )
            (at ?player ?location)
            (at ?target ?location)
            (can_attack_roll ?player ?target)
            (equipped ?player ?weapon)
            (not (attack_roll_success ?player ?target))
        )
        :effect (and 
            (not (can_attack_roll ?player ?target))
            (attack_roll_success ?player ?target)
            (higher_than_ac ?target)
        )
    )

    ; Player succeeds on an attack roll with advantage
    (:action attack_roll_with_advantage
        :parameters (?player - player ?weapon - weapon ?target - object ?location - room)
        :precondition (and 
            (advantage ?weapon)
            (not (disadvantage ?weapon))
            (at ?player ?location)
            (at ?target ?location)
            (can_attack_roll ?player ?target)
            (equipped ?player ?weapon)
            (not (attack_roll_success ?player ?target))
        )
        :effect (and 
            (not (can_attack_roll ?player ?target))
            (attack_roll_success ?player ?target)
            (higher_than_ac ?target)
        )
    )

    ; Player succeeds on an attack roll with disadvantage
    (:action attack_roll_with_disadvantage
        :parameters (?player - player ?weapon - weapon ?target - object ?location - room)
        :precondition (and 
            (not (advantage ?weapon))
            (disadvantage ?weapon)
            (at ?player ?location)
            (at ?target ?location)
            (can_attack_roll ?player ?target)
            (equipped ?player ?weapon)
            (not (attack_roll_success ?player ?target))
        )
        :effect (and 
            (not (can_attack_roll ?player ?target))
            (attack_roll_success ?player ?target)
            (higher_than_ac ?target)
        )
    )

    ; Player damages a target
    (:action damage_roll
        :parameters (?player - player ?target - object ?location - room)
        :precondition (and 
            (at ?player ?location)
            (at ?target ?location)
            (can_damage_roll ?player ?target)
            (alive ?target)
            (higher_than_ac ?target)
        )
        :effect (and 
            (not (can_damage_roll ?player ?target))
            (not (higher_than_ac ?target))
            (damaged ?target)
        )
    )

    ; ================================================================
    ; Basic player actions

    ; Player equips weapon or equipment
    (:action equip
        :parameters (?player - player ?object - object)
        :precondition (and 
            (has ?player ?object)
            (not (equipped ?player ?object))
        )
        :effect (and 
            (equipped ?player ?object)
        )
    )
    
    ; Player unequips weapon or equipment
    (:action unequip
        :parameters (?player - player ?object - object)
        :precondition (and 
            (has ?player ?object)
            (equipped ?player ?object)
        )
        :effect (and 
            (not (equipped ?player ?object))
        )
    )

    ; ================================================================
    ; Movement

    ; Player moves from one room to another
    (:action move
        :parameters (?player - player ?door - door ?location - room ?destination - room)
        :precondition (and 
            (quest)
            (alive ?player)
            (at ?player ?location)
            (connected ?door ?location ?destination)
            (not (locked ?door))
            (forall (?monster - monster)
                (or
                    (not (at ?monster ?location))
                    (and
                        (at ?monster ?location)
                        (not (must_kill ?monster))
                    )
                    (and 
                        (at ?monster ?location)
                        (must_kill ?monster)
                        (not (alive ?monster))
                    )
                )
            )
        )
        :effect (and 
            (not (at ?player ?location))
            (at ?player ?destination)
        )
    )

    ; Player wants to open a door with an ability/skill
    (:action open_door_with_ability
        :parameters (?player - player ?ability - ability ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (dc ?door ?ability)
            (not (action))
        )
        :effect (and 
            (can_ability_check ?player ?ability ?door)
            (action)
        )
    )

    ; Player wants to open a door with equipment
    (:action open_door_with_equipment
        :parameters (?player - player ?equipment - equipment ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (dc_equipment ?door ?equipment)
            (not (action))
        )
        :effect (and 
            (can_equipment_check ?player ?equipment ?door)
            (action)
        )
    )

    ; Player wants to open a door with attack
    (:action open_door_with_attack
        :parameters (?player - player ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (not (action))
        )
        :effect (and 
            (can_attack_roll ?player ?door)
            (action)
        )
    )

    ; Player forces open a door
    (:action force_door
        :parameters (?player - player ?str - ability ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (strength ?str)
            (ability_check_success ?player ?str ?door)
        )
        :effect (and 
            (not (action))
            (not (locked ?door))
            (not (ability_check_success ?player ?str ?door))
        )
    )

    ; Player uses a switch to open a door
    (:action use_door_switch
        :parameters (?player - player ?perception - skill ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (perception ?perception)
            (ability_check_success ?player ?perception ?door)
        )
        :effect (and 
            (not (action))
            (not (locked ?door))
            (not (ability_check_success ?player ?perception ?door))
        )
    )

    ; Player uses thieves tools to open a door
    (:action use_thieves_tools
        :parameters (?player - player ?thieves_tools - equipment ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (equipped ?player ?thieves_tools)
            (thieves_tools ?thieves_tools)
            (equipment_check_success ?player ?thieves_tools)
        )
        :effect (and 
            (not (action))
            (not (locked ?door))
            (not (equipped ?player ?thieves_tools))
            (not (equipment_check_success ?player ?thieves_tools))
        )
    )
    
    ; Player attacks a door
    (:action attack_door
        :parameters (?player - player ?weapon - weapon ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (equipped ?player ?weapon)
            (attack_roll_success ?player ?door)
        )
        :effect (and 
            (can_damage_roll ?player ?door)
            (not (attack_roll_success ?player ?door))
        )
    )

    ; Player breaks down a door
    (:action breaks_down_door
        :parameters (?player - player ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (damaged ?door)
        )
        :effect (and 
            (not (action))
            (not (locked ?door))
            (not (alive ?door))
        )
    )

    ; ================================================================
    ; NPCs

    ; Player receives quest from NPC that can give quests
    (:action receive_quest
        :parameters (?player - player ?npc - npc ?friendly - friendly ?location - room)
        :precondition (and
            (alive ?player)
            (alive ?npc)
            (at ?player ?location)
            (at ?npc ?location)
            (gives_quest ?npc)
            (attitude_towards_player ?npc ?friendly)
        )
        :effect (and
            (quest)
        )
    )

    ; Player roleplays positively, which improves the NPC's attitude towards the player
    (:action roleplay_positively
        :parameters (?player - player ?npc - npc ?current - attitude ?next - attitude ?location - room)
        :precondition (and
            (alive ?player)
            (alive ?npc)
            (at ?player ?location)
            (at ?npc ?location)
            (attitude_towards_player ?npc ?current)
            (improve_attitude ?current ?next)
        )
        :effect (and
            (not (attitude_towards_player ?npc ?current))
            (attitude_towards_player ?npc ?next)
        )
    )

    ; Player roleplays negatively, which degrades the NPC's attitude towards the player
    (:action roleplay_negatively
        :parameters (?player - player ?npc - npc ?current - attitude ?next - attitude ?location - room)
        :precondition (and
            (alive ?player)
            (alive ?npc)
            (at ?player ?location)
            (at ?npc ?location)
            (attitude_towards_player ?npc ?current)
            (degrade_attitude ?current ?next)
        )
        :effect (and
            (not (attitude_towards_player ?npc ?current))
            (attitude_towards_player ?npc ?next)
        )
    )

    ; ================================================================
    ; Combat

    ; Player wants to attack another entity
    (:action declare_attack_against_entity
        :parameters (?player - player ?target - entity ?location - room)
        :precondition (and 
            (alive ?player)
            (alive ?target)
            (at ?player ?location)
            (at ?target ?location)
            (not (action))
        )
        :effect (and 
            (can_attack_roll ?player ?target)
            (action)
        )
    )

    ; Player attacks a monster
    (:action attack_monster
        :parameters (?player - player ?weapon - weapon ?monster - monster ?location - room)
        :precondition (and 
            (action)
            (alive ?player)
            (alive ?monster)
            (at ?player ?location)
            (at ?monster ?location)
            (equipped ?player ?weapon)
            (attack_roll_success ?player ?monster)
        )
        :effect (and 
            (combat)
            (can_damage_roll ?player ?monster)
            (not (attack_roll_success ?player ?monster))
        )
    )

    ; Player kills a monster
    (:action kill_monster
        :parameters (?player - player ?monster - monster ?location - room)
        :precondition (and 
            (action)
            (combat)
            (alive ?player)
            (alive ?monster)
            (at ?player ?location)
            (at ?monster ?location)
            (damaged ?monster)
        )
        :effect (and 
            (not (action))
            (not (combat))
            (not (alive ?monster))
        )
    )
)
""".format(d=self.domain))

    def build_problem(self) -> None:
        logger.debug("Building problem")
        problem_file = os.path.join(
            Config.directory.planning,
            "{u}.{p}.problem.pddl".format(u=Config.uuid, p=self.problem))

        with open(problem_file, 'w') as writer:
            ################################################
            # Construct the problem file header
            writer.write(self._construct_problem_header(
                self.problem, "player"))

            ################################################
            # Construct the problem file objects
            objects = []

            # Player
            objects.append(("player", "player"))
            for intent in State.get_dm().player_intent_map.keys():
                objects.append((intent, "intent"))
            for item in State.get_all_item_ids():
                objects.append((item, "item"))

            # NPCs
            for npc in State.get_dm().npcs.get_all_npcs():
                objects.append((npc.id, "npc"))
            objects.append(("indifferent", "indifferent"))
            objects.append(("friendly", "friendly"))
            objects.append(("hostile", "hostile"))

            # Rooms
            for room in State.get_dm().adventure.get_all_rooms():
                objects.append((room.id, "room"))

            # Doors
            doors = []
            for room in State.get_dm().adventure.get_all_rooms():
                for connection in room.get_connected_rooms():
                    door = "{r}---{c}".format(r=room.id, c=connection)
                    reverse_door = "{c}---{r}".format(r=room.id, c=connection)
                    if not reverse_door in doors:
                        doors.append(door)
            for door in doors:
                objects.append((door, "door"))

            # Monsters
            for monster in State.get_dm().npcs.get_all_monsters():
                objects.append((monster.unique_id, monster.id))

            # Abilities
            for ability in Abilities.get_all_abilities():
                objects.append((ability[0], "ability"))

            # Skills
            for skill in Skills.get_all_skills():
                objects.append((skill[0], "skill"))

            # Weapons
            for weapon in State.get_player().get_all_weapon_ids():
                objects.append((weapon, "weapon"))

            # Equipment
            for equipment in State.get_player().get_all_equipment_ids():
                objects.append((equipment, "equipment"))

            # Puzzles
            for room in State.get_dm().adventure.get_all_rooms():
                for puzzle in room.puzzles.get_all_puzzles():
                    if not puzzle.type == "door":
                        objects.append((puzzle.id, "puzzle"))

            # Construct the string
            writer.write(self._construct_objects(objects))

            ################################################
            # Construct the problem file init
            init = []

            # Adventure
            if State.questing:
                init.append(("quest"))

            # Player
            init.append(("at", "player", State.get_current_room().id))
            if State.is_alive():
                init.append(("alive", "player"))
            for ability in Abilities.get_all_abilities():
                init.append((ability[1].lower(), ability[0]))
            for skill in Skills.get_all_skills():
                init.append((skill[0], skill[0]))
            for weapon in State.get_player().get_all_weapon_ids():
                init.append(("has", "player", weapon))
            for equipment in State.get_player().get_all_equipment_ids():
                init.append((equipment, equipment))
                init.append(("has", "player", equipment))

            # NPCs
            for npc in State.get_dm().npcs.get_all_npcs():
                init.append(("at", npc.id, State.get_current_room(npc.id).id))
                if State.is_alive(npc.id):
                    init.append(("alive", npc.id))
                if npc.gives_quest:
                    init.append(("gives_quest", npc.id))
            init.append(("improve_attitude", "indifferent", "friendly"))
            init.append(("improve_attitude", "hostile", "indifferent"))
            init.append(("degrade_attitude", "friendly", "indifferent"))
            init.append(("degrade_attitude", "indifferent", "hostile"))
            for npc in State.get_dm().npcs.get_all_npcs():
                init.append(("attitude_towards_player", npc.id, npc.attitude))

            # Monsters
            for monster in State.get_dm().npcs.get_all_monsters():
                init.append(("at", monster.unique_id,
                             State.get_current_room(monster.unique_id).id))
            for monster in State.get_dm().npcs.get_all_monsters():
                if State.is_alive(monster.unique_id):
                    init.append(("alive", monster.unique_id))

            # Combat
            for npc in State.get_dm().npcs.get_all_npcs():
                if npc.must_kill:
                    init.append(("must_kill", npc.id))
            for monster in State.get_dm().npcs.get_all_monsters():
                if monster.must_kill:
                    init.append(("must_kill", monster.unique_id))

            # Rooms
            for door in doors:
                room1 = door.split("---")[0]
                room2 = door.split("---")[1]
                init.append(("connected", door, room1, room2))
                init.append(("connected", door, room2, room1))
                init.append(("at", door, room1))
                init.append(("at", door, room2))
                if not State.travel_allowed(room1, room2):
                    init.append(("locked", door))
                if not State.connection_broken(room1, room2):
                    init.append(("alive", door))

            # Puzzles
            for room in State.get_dm().adventure.get_all_rooms():
                for puzzle in room.puzzles.get_all_puzzles():
                    # Ability solution
                    for ability in Abilities.get_all_abilities():
                        if puzzle.check_solution_ability(ability[0]):
                            init.append(("dc", puzzle.id, ability[0]))
                    # Skill solution
                    for skill in Skills.get_all_skills():
                        if puzzle.check_solution_skill(skill[0]):
                            init.append(("dc", puzzle.id, skill[0]))
                    # Equipment solution
                    for equipment in State.get_player().get_all_equipment_ids(
                    ):
                        if puzzle.check_solution_equipment(equipment):
                            init.append(("dc_equipment", puzzle.id, equipment))
                    # Intent solution
                    for intent in State.get_dm().player_intent_map.keys():
                        if puzzle.check_solution_intent(intent):
                            init.append(("intent_solution", puzzle.id, intent))
                    # Item solution
                    for item in State.get_all_item_ids():
                        if puzzle.check_solution_item(item):
                            init.append(("item_solution", puzzle.id, item))

                    # TODO add spell solution

            # Construct the string
            writer.write(self._construct_init(init))

            ################################################
            # Construct the problem file goal
            goal = []
            goal.append(State.current_goal)
            writer.write(self._construct_goal(goal))
            writer.write(self._construct_problem_footer())
