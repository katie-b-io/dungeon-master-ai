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
        ; Entity is alive
        (alive ?entity - entity)
        ; Entity is in a room
        (at ?entity - entity ?room - room)
        ; Entity has a weapon
        (armed ?entity - entity ?weapon - weapon)
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
        (can_ability_check ?entity - entity ?ability - ability)
        ; Entity can perform an equipment check
        (can_equipment_check ?entity - entity ?equipment - equipment)
        ; Entity makes a successful ability check
        (ability_check_success ?entity - entity ?ability - ability)
        ; Entity makes a successful equipment check
        (equipment_check_success ?entity - entity ?equipment - equipment)
        ; Entity makes a successful attack roll against target
        (attack_roll_success ?entity - entity ?target - object)
        ; Tools
        (thieves_tools ?equipment - equipment)
        ; Action is performed
        (action)
    )

    ; Entity succeeds on an ability check
    (:action ability_check
        :parameters (?entity - entity ?ability - ability)
        :precondition (and 
            (can_ability_check ?entity ?ability)
            (not (ability_check_success ?entity ?ability))
        )
        :effect (and 
            (not (can_ability_check ?entity ?ability))
            (ability_check_success ?entity ?ability)
        )
    )
    
    ; Entity succeeds on an equipment check
    (:action equipment_check
        :parameters (?entity - entity ?equipment - equipment)
        :precondition (and 
            (can_equipment_check ?entity ?equipment)
            (not (equipment_check_success ?entity ?equipment))
        )
        :effect (and 
            (not (can_equipment_check ?entity ?equipment))
            (equipment_check_success ?entity ?equipment)
        )
    )

    ; Entity succeeds on an attack roll
    (:action attack_roll
        :parameters (?entity - entity ?target - object)
        :precondition (and 
            (can_attack_roll ?entity ?target)
            (not (attack_roll_success ?entity ?target))
        )
        :effect (and 
            (not (can_attack_roll ?entity ?target))
            (attack_roll_success ?entity ?target)
        )
    )

    ; An entity damages a target
    (:action damage_roll
        :parameters (?entity - entity ?target - target)
        :precondition (and 
            (can_damage_roll ?entity ?target)
            (hp ?target)
            (ac ?target)
        )
        :effect (and 
            (not (can_damage_roll ?entity ?target))
            (not (hp ?target))
        )
    )

    ; An entity moves from one room to another
    (:action move
        :parameters (?entity - entity ?door - door ?location - room ?destination - room)
        :precondition (and 
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
            (connected ?door ?location ?destination)
            (locked ?door)
            (dc ?door ?ability)
            (not (action))
        )
        :effect (and 
            (can_ability_check ?player ?ability)
            (action)
        )
    )

    ; An entity wants to open a door with equipment
    (:action open_door_with_equipment
        :parameters (?player - player ?equipment - equipment ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (dc_equipment ?door ?equipment)
            (not (action))
        )
        :effect (and 
            (can_equipment_check ?player ?equipment)
            (action)
        )
    )

    ; An entity wants to open a door with attack
    (:action open_door_with_attack
        :parameters (?player - player ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
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
            (connected ?door ?location ?destination)
            (locked ?door)
            (strength ?str)
            (ability_check_success ?player ?str)
        )
        :effect (and 
            (not (action))
            (not (locked ?door))
            (not (ability_check_success ?player ?str))
        )
    )

    ; A player uses the switch to open a door
    (:action use_door_switch
        :parameters (?player - player ?perception - skill ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (perception ?perception)
            (ability_check_success ?player ?perception)
        )
        :effect (and 
            (not (action))
            (not (locked ?door))
            (not (ability_check_success ?player ?perception))
        )
    )

    ; A player uses thieves tools to open a door
    (:action use_thieves_tools
        :parameters (?player - player ?thieves_tools - equipment ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (thieves_tools ?thieves_tools)
            (equipment_check_success ?player ?thieves_tools)
        )
        :effect (and 
            (not (action))
            (not (locked ?door))
            (not (equipment_check_success ?player ?thieves_tools))
        )
    )
    
    ; An player attacks a door
    (:action attack_door
        :parameters (?player - player ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (attack_roll_success ?player ?door)
        )
        :effect (and 
            (can_damage_roll ?player ?door)
        )
    )

    ; An player breaks down a door
    (:action breaks_down_door
        :parameters (?player - player ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (not (hp ?door))
        )
        :effect (and 
            (not (action))
            (not (locked ?door))
        )
    )


)