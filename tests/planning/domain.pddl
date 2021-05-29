;Dungeons and Dragons 5th Edition Domain

(define (domain dnd)

    ;remove requirements that are not needed
    (:requirements 
        :strips
        :action-costs
        :typing
        :conditional-effects
        :negative-preconditions
        :equality
    )

    (:types 
        ; Entities exist
        entity - object
        player npc monster - entity
        ; Roleplaying exists
        attitude - object
        neutral positive negative - attitude
        ; Monsters exist
        cat giant_rat goblin skeleton zombie - monster
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
        ; Attacks exist
        attack - object
        ; Damage vulnerabilities exist
        damage_vulnerability - object
        ; Damage immunities exist
        damage_immunity - object
        ; Condition immunities exist
        condition_immunity - object
        ; Languages exist
        language - object
    )

    ; un-comment following line if constants are needed
    ;(:constants )

    (:predicates 
        ; Adventure
        (quest) ; player has received quest
        (dwarven_thrower) ; player has found dwarven thrower treasure
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
        ; Entity is alive
        (alive ?entity - entity)
        ; Object is equipped
        (equipped ?entity - entity ?object - object)
        ; Rooms are connected
        (connected ?door - door ?location - room ?destination - room)
        ; Door is locked
        (locked ?door - door)
        ; DC of object
        (dc ?target - object ?ability - ability)
        (dc_equipment ?target - object ?equipment - equipment)
        ; HP of object
        (hp ?target - object)
        ; AC of object
        (ac ?target - object)
        ; Entity can perform an attack roll
        (can_attack_roll ?entity - entity ?target - object)
        ; Entity can perform a damage roll
        (can_damage_roll ?entity - entity ?target - object)
        ; Entity can perform an ability check
        (can_ability_check ?entity - entity ?ability - ability ?target - object)
        ; Entity can perform an equipment check
        (can_equipment_check ?entity - entity ?equipment - equipment ?target - object)
        ; Entity makes a successful ability check
        (ability_check_success ?entity - entity ?ability - ability ?target - object)
        ; Entity makes a successful equipment check
        (equipment_check_success ?entity - entity ?equipment - equipment)
        ; Entity makes a successful attack roll against target
        (attack_roll_success ?entity - entity ?target - object)
        ; Tools
        (thieves_tools ?equipment - equipment)
        ; Action is performed
        (action)
        ; NPC attitudes
        (attitude_towards_player ?npc - npc ?attitude - attitude)
        (improve_attitude ?current - attitude ?next - attitude)
        (degrade_attitude ?current - attitude ?next - attitude)
    )

    ; ================================================================
    ; Rolls

    ; Entity succeeds on an ability check
    (:action ability_check
        :parameters (?entity - entity ?ability - ability ?target - object ?location - room)
        :precondition (and 
            (at ?entity ?location)
            (at ?target ?location)
            (can_ability_check ?entity ?ability ?target)
            (not (ability_check_success ?entity ?ability ?target))
        )
        :effect (and 
            (not (can_ability_check ?entity ?ability ?target))
            (ability_check_success ?entity ?ability ?target)
        )
    )
    
    ; Entity succeeds on an equipment check
    (:action equipment_check
        :parameters (?entity - entity ?equipment - equipment ?target - object ?location - room)
        :precondition (and 
            (at ?entity ?location)
            (at ?target ?location)
            (can_equipment_check ?entity ?equipment ?target)
            (not (equipment_check_success ?entity ?equipment))
        )
        :effect (and 
            (not (can_equipment_check ?entity ?equipment ?target))
            (equipment_check_success ?entity ?equipment)
        )
    )

    ; Entity succeeds on an attack roll
    (:action attack_roll
        :parameters (?entity - entity ?weapon - weapon ?target - object ?location - room)
        :precondition (and 
            (at ?entity ?location)
            (at ?target ?location)
            (can_attack_roll ?entity ?target)
            (equipped ?entity ?weapon)
            (not (attack_roll_success ?entity ?target))
        )
        :effect (and 
            (not (can_attack_roll ?entity ?target))
            (attack_roll_success ?entity ?target)
        )
    )

    ; An entity damages a target
    (:action damage_roll
        :parameters (?entity - entity ?target - object ?location - room)
        :precondition (and 
            (at ?entity ?location)
            (at ?target ?location)
            (can_damage_roll ?entity ?target)
            (hp ?target)
            (ac ?target)
        )
        :effect (and 
            (not (can_damage_roll ?entity ?target))
            (not (hp ?target))
        )
    )

    ; ================================================================
    ; Basic player actions
    (:action equip
        :parameters (?entity - entity ?object - object)
        :precondition (and 
            (has ?entity ?object)
            (not (equipped ?entity ?object))
        )
        :effect (and 
            (equipped ?entity ?object)
        )
    )
    
    (:action unequip
        :parameters (?entity - entity ?object - object)
        :precondition (and 
            (has ?entity ?object)
            (equipped ?entity ?object)
        )
        :effect (and 
            (not (equipped ?entity ?object))
        )
    )

    ; ================================================================
    ; Movement

    ; An entity moves from one room to another
    (:action move
        :parameters (?entity - entity ?door - door ?location - room ?destination - room)
        :precondition (and 
            (quest)
            (alive ?entity)
            (at ?entity ?location)
            (connected ?door ?location ?destination)
            (not (locked ?door))
        )
        :effect (and 
            (not (at ?entity ?location))
            (at ?entity ?destination)
        )
    )

    ; An entity wants to open a door with an ability/skill
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

    ; An entity wants to open a door with equipment
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

    ; An entity wants to open a door with attack
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

    ; A player forces open a door
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

    ; A player uses the switch to open a door
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

    ; A player uses thieves tools to open a door
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
    
    ; A player attacks a door
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

    ; A player breaks down a door
    (:action breaks_down_door
        :parameters (?player - player ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (not (hp ?door))
        )
        :effect (and 
            (not (action))
            (not (locked ?door))
        )
    )

    ; ================================================================
    ; NPCs
    (:action receive_quest
        :parameters (?player - player ?corvus - npc ?positive - positive ?location - room)
        :precondition (and
            (alive ?player)
            (alive ?corvus)
            (at ?player ?location)
            (at ?corvus ?location)
            (attitude_towards_player ?corvus ?positive)
        )
        :effect (and
            (quest)
        )
    )

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


)