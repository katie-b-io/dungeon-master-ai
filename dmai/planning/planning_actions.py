planning_actions = {
    "ability_check": """
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
)""",

    "ability_check_with_advantage": """
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
)""",

    "ability_check_with_disadvantage": """
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
)""",

    "equipment_check": """
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
)""",

    "equipment_check_with_advantage": """
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
)""",

    "equipment_check_with_disadvantage": """
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
)""",

    "attack_roll": """
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
    )
)""",

    "attack_roll_with_advantage": """
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
    )
)""",

    "attack_roll_with_disadvantage": """
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
    )
)""",

    "damage_roll": """
; Entity damages a target
(:action damage_roll
    :parameters (?entity - entity ?target - object ?location - room)
    :precondition (and 
        (at ?entity ?location)
        (at ?target ?location)
        (can_damage_roll ?entity ?target)
        (alive ?target)
        (higher_than_ac ?target)
    )
    :effect (and 
        (not (can_damage_roll ?entity ?target))
        (not (higher_than_ac ?target))
        (damaged ?target)
    )
)""",

    "equip": """
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
)""",

    "unequip": """
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
)""",

    "move": """
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
)""",

    "open_door_with_ability": """
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
    )
    :effect (and 
        (can_ability_check ?player ?ability ?door)
        (action)
    )
)""",

    "open_door_with_equipment": """
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
    )
    :effect (and 
        (can_equipment_check ?player ?equipment ?door)
        (action)
    )
)""",

    "open_door_with_attack": """
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
)""",

    "force_door": """
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
)""",

    "use_door_switch": """
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
)""",

    "use_thieves_tools": """
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
    )
    :effect (and 
        (not (action))
        (not (locked ?door))
        (not (equipped ?player ?thieves_tools))
        (not (equipment_check_success ?player ?thieves_tools ?door))
    )
)""",

    "attack_door": """
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
)""",

    "breaks_down_door": """
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
)""",

    "receive_quest": """
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
)""",

    "roleplay_positively": """
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
)""",

    "roleplay_negatively": """
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
)""",

    "declare_attack_against_entity": """
; Entity wants to attack another entity
(:action declare_attack_against_entity
    :parameters (?entity - entity ?target - entity ?location - room)
    :precondition (and 
        (alive ?entity)
        (alive ?target)
        (at ?entity ?location)
        (at ?target ?location)
        (not (action))
    )
    :effect (and 
        (can_attack_roll ?entity ?target)
        (action)
    )
)""",

    "attack_monster": """
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
)""",

    "attack_player": """
; Monster attacks a player
(:action attack_player
    :parameters (?monster - monster ?weapon - weapon ?player - player ?location - room)
    :precondition (and 
        (action)
        (alive ?monster)
        (alive ?player)
        (at ?monster ?location)
        (at ?player ?location)
        (equipped ?monster ?weapon)
        (attack_roll_success ?monster ?player)
    )
    :effect (and 
        (combat)
        (can_damage_roll ?monster ?player)
        (not (attack_roll_success ?monster ?player))
    )
)""",

    "kill_monster": """
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
)""",

    "kill_player": """
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
)"""
}