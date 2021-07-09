from dmai.nlg.nlg import NLG
from dmai.game.state import self.state
from dmai.domain.actions.actions import Actions

planning_actions = {
    "ability_check": {
        "pddl": """
; Entity succeeds on an ability check
(:action ability_check
    :parameters (?entity - entity ?ability - ability ?target - object ?location - room)
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
        (at ?entity ?location)
        (at ?target ?location)
        (can_ability_check ?entity ?ability ?target)
        (not (ability_check_success ?entity ?ability ?target))
    )
    :effect (and 
        (not (can_ability_check ?entity ?ability ?target))
        (ability_check_success ?entity ?ability ?target)
    )
)"""},

    "ability_check_with_advantage": {
        "pddl": """
; Entity succeeds on an ability check with advantage
(:action ability_check_with_advantage
    :parameters (?entity - entity ?ability - ability ?target - object ?location - room)
    :precondition (and 
        (advantage ?ability)
        (not (disadvantage ?ability))
        (at ?entity ?location)
        (at ?target ?location)
        (can_ability_check ?entity ?ability ?target)
        (not (ability_check_success ?entity ?ability ?target))
    )
    :effect (and 
        (not (can_ability_check ?entity ?ability ?target))
        (ability_check_success ?entity ?ability ?target)
    )
)"""},

    "ability_check_with_disadvantage": {
        "pddl": """
; Entity succeeds on an ability check with disadvantage
(:action ability_check_with_disadvantage
    :parameters (?entity - entity ?ability - ability ?target - object ?location - room)
    :precondition (and 
        (not (advantage ?ability))
        (disadvantage ?ability)
        (at ?entity ?location)
        (at ?target ?location)
        (can_ability_check ?entity ?ability ?target)
        (not (ability_check_success ?entity ?ability ?target))
    )
    :effect (and 
        (not (can_ability_check ?entity ?ability ?target))
        (ability_check_success ?entity ?ability ?target)
    )
)"""},

    "equipment_check": {
        "pddl": """
; Entity succeeds on an equipment check
(:action equipment_check
    :parameters (?entity - entity ?equipment - equipment ?target - object ?location - room)
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
        (at ?entity ?location)
        (at ?target ?location)
        (can_equipment_check ?entity ?equipment ?target)
        (not (equipment_check_success ?entity ?equipment ?target))
    )
    :effect (and 
        (not (can_equipment_check ?entity ?equipment ?target))
        (equipment_check_success ?entity ?equipment ?target)
    )
)"""},

    "equipment_check_with_advantage": {
        "pddl": """
; Entity succeeds on an equipment check with advantage
(:action equipment_check_with_advantage
    :parameters (?entity - entity ?equipment - equipment ?target - object ?location - room)
    :precondition (and 
        (advantage ?equipment)
        (not (disadvantage ?equipment))
        (at ?entity ?location)
        (at ?target ?location)
        (can_equipment_check ?entity ?equipment ?target)
        (not (equipment_check_success ?entity ?equipment ?target))
    )
    :effect (and 
        (not (can_equipment_check ?entity ?equipment ?target))
        (equipment_check_success ?entity ?equipment ?target)
    )
)"""},

    "equipment_check_with_disadvantage": {
        "pddl": """
; Entity succeeds on an equipment check with disadvantage
(:action equipment_check_with_disadvantage
    :parameters (?entity - entity ?equipment - equipment ?target - object ?location - room)
    :precondition (and 
        (not (advantage ?equipment))
        (disadvantage ?equipment)
        (at ?entity ?location)
        (at ?target ?location)
        (can_equipment_check ?entity ?equipment ?target)
        (not (equipment_check_success ?entity ?equipment ?target))
    )
    :effect (and 
        (not (can_equipment_check ?entity ?equipment ?target))
        (equipment_check_success ?entity ?equipment ?target)
    )
)"""},

    "attack_roll": {
        "func": Actions.attack_roll,
        "pddl": """
; Entity succeeds on an attack roll
(:action attack_roll
    :parameters (?entity - entity ?weapon - weapon ?target - object ?location - room)
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
        (at ?entity ?location)
        (at ?target ?location)
        (can_attack_roll ?entity ?target)
        (equipped ?entity ?weapon)
        (not (attack_roll_success ?entity ?target))
    )
    :effect (and 
        (not (can_attack_roll ?entity ?target))
        (attack_roll_success ?entity ?target)
        (higher_than_ac ?target)
        (can_damage_roll ?entity ?target)
    )
)"""},

    "attack_roll_with_advantage": {
        "pddl": """
; Entity succeeds on an attack roll with advantage
(:action attack_roll_with_advantage
    :parameters (?entity - entity ?weapon - weapon ?target - object ?location - room)
    :precondition (and 
        (advantage ?weapon)
        (not (disadvantage ?weapon))
        (at ?entity ?location)
        (at ?target ?location)
        (can_attack_roll ?entity ?target)
        (equipped ?entity ?weapon)
        (not (attack_roll_success ?entity ?target))
    )
    :effect (and 
        (not (can_attack_roll ?entity ?target))
        (attack_roll_success ?entity ?target)
        (higher_than_ac ?target)
        (can_damage_roll ?entity ?target)
    )
)"""},

    "attack_roll_with_disadvantage": {
        "pddl": """
; Entity succeeds on an attack roll with disadvantage
(:action attack_roll_with_disadvantage
    :parameters (?entity - entity ?weapon - weapon ?target - object ?location - room)
    :precondition (and 
        (not (advantage ?weapon))
        (disadvantage ?weapon)
        (at ?entity ?location)
        (at ?target ?location)
        (can_attack_roll ?entity ?target)
        (equipped ?entity ?weapon)
        (not (attack_roll_success ?entity ?target))
    )
    :effect (and 
        (not (can_attack_roll ?entity ?target))
        (attack_roll_success ?entity ?target)
        (higher_than_ac ?target)
        (can_damage_roll ?entity ?target)
    )
)"""},

    "damage_roll": {
        "func": Actions.damage_roll,
        "pddl": """
; Entity damages a target
(:action damage_roll
    :parameters (?entity - entity ?weapon - weapon ?target - object ?location - room)
    :precondition (and 
        (at ?entity ?location)
        (at ?target ?location)
        (can_damage_roll ?entity ?target)
        (alive ?target)
        (higher_than_ac ?target)
        (equipped ?entity ?weapon)
    )
    :effect (and 
        (not (can_damage_roll ?entity ?target))
        (not (higher_than_ac ?target))
        (damaged ?target)
        (not (attack_roll_success ?entity ?target))
    )
)"""},

    "equip": {
        "pddl": """
; Entity equips weapon or equipment
(:action equip
    :parameters (?entity - entity ?object - object)
    :precondition (and 
        (has ?entity ?object)
        (not (equipped ?entity ?object))
    )
    :effect (and 
        (equipped ?entity ?object)
    )
)"""},

    "unequip": {
        "pddl": """
; Entity unequips weapon or equipment
(:action unequip
    :parameters (?entity - entity ?object - object)
    :precondition (and 
        (has ?entity ?object)
        (equipped ?entity ?object)
    )
    :effect (and 
        (not (equipped ?entity ?object))
    )
)"""},
    
    "explore": {
        "pddl": """
; Player explores room
(:action explore
    :parameters (?player - player ?location - room)
    :precondition (and 
        (at ?player ?location)
        (treasure ?location)
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
        (not (treasure ?location))
    )
)"""},

    "use_potion_of_healing": {
        "pddl": """
; Player drinks potion of healing
(:action use_potion_of_healing
    :parameters (?player - player ?item - item)
    :precondition (and 
        (potion_of_healing ?item)
        (injured ?player)
        (has ?player ?item)
    )
    :effect (and 
        (not (has ?player ?item))
        (not (injured ?player))
    )
)"""},
    
    "move": {
        "pddl": """
; Player moves from one room to another
(:action move
    :parameters (?player - player ?door - door ?location - room ?destination - room)
    :precondition (and 
        (quest)
        (alive ?player)
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (not (treasure ?location))
        (or 
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
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
)"""},

    "open_door_with_ability": {
        "pddl": """
; Player wants to open a door with an ability/skill
(:action open_door_with_ability
    :parameters (?player - player ?ability - ability ?door - door ?location - room ?destination - room)
    :precondition (and 
        (alive ?player)
        (at ?player ?location)
        (at ?door ?location)
        (connected ?door ?location ?destination)
        (locked ?door)
        (ability_solution ?door ?ability)
        (not (action))
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (or 
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
    )
    :effect (and 
        (can_ability_check ?player ?ability ?door)
        (action)
    )
)"""},

    "open_door_with_equipment": {
        "pddl": """
; Player wants to open a door with equipment
(:action open_door_with_equipment
    :parameters (?player - player ?equipment - equipment ?door - door ?location - room ?destination - room)
    :precondition (and 
        (alive ?player)
        (at ?player ?location)
        (at ?door ?location)
        (connected ?door ?location ?destination)
        (locked ?door)
        (equipment_solution ?door ?equipment)
        (not (action))
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (or 
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
    )
    :effect (and 
        (can_equipment_check ?player ?equipment ?door)
        (action)
    )
)"""},

    "open_door_with_attack": {
        "pddl": """
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
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (or 
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
    )
    :effect (and 
        (can_attack_roll ?player ?door)
        (action)
    )
)"""},

    "force_door": {
        "pddl": """
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
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (or 
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
    )
    :effect (and 
        (not (action))
        (not (locked ?door))
        (not (ability_check_success ?player ?str ?door))
    )
)"""},

    "use_door_switch": {
        "pddl": """
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
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (or 
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
    )
    :effect (and 
        (not (action))
        (not (locked ?door))
        (not (ability_check_success ?player ?perception ?door))
    )
)"""},

    "use_thieves_tools": {
        "pddl": """
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
        (equipment_check_success ?player ?thieves_tools ?door)
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (or 
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
    )
    :effect (and 
        (not (action))
        (not (locked ?door))
        (not (equipped ?player ?thieves_tools))
        (not (equipment_check_success ?player ?thieves_tools ?door))
    )
)"""},

    "attack_door": {
        "pddl": """
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
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (or 
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
    )
    :effect (and 
        (can_damage_roll ?player ?door)
        (not (attack_roll_success ?player ?door))
    )
)"""},

    "breaks_down_door": {
        "pddl": """
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
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (or 
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
    )
    :effect (and 
        (not (action))
        (not (locked ?door))
        (not (alive ?door))
    )
)"""},
    
    "light_torch": {
        "pddl": """
; Player lights a torch
(:action light_torch
    :parameters (?player - player ?torch - equipment)
    :precondition (and 
        (alive ?player)
        (torch ?torch)
        (has ?player ?torch)
    )
    :effect (and
        (torch_lit)
    )
)"""},

    "extinguish_torch": {
        "pddl": """
    ; Extinguish torch
    (:action extinguish_torch
        :parameters (?player - player ?torch - equipment)
        :precondition (and 
            (alive ?player)
            (torch ?torch)
            (has ?player ?torch)
            (torch_lit)
        )
        :effect (and
            (when (not (darkvision))
                (not (torch_lit))
            )
        )
    )"""},
    
    "receive_quest": {
        "pddl": """
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
)"""},

    "roleplay_positively": {
        "pddl": """
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
)"""},

    "roleplay_negatively": {
        "pddl": """
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
)"""},

    "declare_attack_against_entity": {
        "pddl": """
; Player wants to attack another entity
(:action declare_attack_against_entity
    :parameters (?player - player ?target - entity ?location - room)
    :precondition (and 
        (alive ?player)
        (alive ?target)
        (at ?player ?location)
        (at ?target ?location)
        (not (action))
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
        (or
            (not (injured ?player))
            (and
                (injured ?player)
                (forall (?item - item)
                    (and
                        (not (potion_of_healing ?item))
                        (not (has ?player ?item))
                    )
                )
            )
        )
    )
    :effect (and 
        (can_attack_roll ?player ?target)
        (action)
        (combat)
    )
)"""},

    "kill_monster": {
        "pddl": """
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
)"""},

    "declare_attack_against_player": {
        "func": Actions.declare_attack_against_player,
        "pddl": """
; Monster wants to attack player
(:action declare_attack_against_player
    :parameters (?monster - monster ?player - player ?location - room)
    :precondition (and 
        (alive ?monster)
        (alive ?player)
        (at ?monster ?location)
        (at ?player ?location)
        (not (action))
        (or
            (not (dark ?location))
            (or (torch_lit) (darkvision))
        )
    )
    :effect (and 
        (can_attack_roll ?monster ?player)
        (action)
        (combat)
    )
)"""},
    
    "kill_player": {
        "func": self.state.update_initiative_order,
        "pddl": """
; Monster kills a player
(:action kill_player
    :parameters (?monster - monster ?player - player ?location - room)
    :precondition (and 
        (action)
        (combat)
        (alive ?monster)
        (alive ?player)
        (at ?monster ?location)
        (at ?player ?location)
        (damaged ?player)
    )
    :effect (and 
        (not (action))
        (not (combat))
        (not (alive ?player))
    )
)"""}
}