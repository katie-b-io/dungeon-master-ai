;Dungeons and Dragons 5th Edition Domain

(define (domain dnd)

    ;remove requirements that are not needed
    (:requirements 
        :strips
        :fluents
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
        ; Abilities exist
        ability - object
        ; Skills exist
        skill - object
        ; Rooms exist
        room - object
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
        ; Ability is strength
        (strength ?ability - ability)
        ; Skill is perception
        (perception ?skill - skill)
        ; Entity is alive
        (alive ?entity - entity)
        ; Entity is in a room
        (at ?entity - entity ?room - room)
        ; Entity has a weapon
        ; (armed ?entity - entity ?weapon - weapon)
        ; Rooms are connected
        (connected ?location - room ?destination - room)
        ; Connection between rooms is locked
        (locked ?location - room ?destination - room)
    )

    (:functions
        ; Calculate ability check for entity
        (ability_check ?entity - entity ?ability - ability) - number
        ; Calculate skill check for entity
        (skill_check ?entity - entity ?skill - skill) - number
        ; Calculate attack roll for entity
        (attack_roll ?entity - entity) - number
        ; Calculate damage being produced by entity
        (damage ?entity - entity) - number
        ; Calculate HP for entity
        (hp ?entity - entity) - number
        ; Calculate AC for entity
        (ac ?entity - entity) - number
        ; Calculate DC for door
        (dc_door_str ?str - ability ?location - room ?destination - room) - number
        (dc_door_perception ?perception - skill ?location - room ?destination - room) - number
        ; Calculate HP for door
        (hp_door ?location - room ?destination - room) - number
        ; Calculate AC for door
        (ac_door ?location - room ?destination - room) - number
    )

    ; An entity moves from one room to another
    (:action move
        :parameters (?entity - entity ?location - room ?destination - room)
        :precondition (and 
            (alive ?entity)
            (at ?entity ?location)
            (connected ?location ?destination)
            (not (locked ?location ?destination))
        )
        :effect (and 
            (not (at ?entity ?location))
            (at ?entity ?destination)
        )
    )

    ; An player forces open a door
    (:action force_door
        :parameters (?player - player ?str - ability ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (connected ?location ?destination)
            (locked ?location ?destination)
            (strength ?str)
            (>= (dc_door_str ?str ?location ?destination) (ability_check ?player ?str))
        )
        :effect (and 
            (not (locked ?location ?destination))
            (not (locked ?destination ?location))
        )
    )

    ; An player uses the switch to open a door
    (:action use_door_switch
        :parameters (?player - player ?perception - skill ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (connected ?location ?destination)
            (locked ?location ?destination)
            (perception ?perception)
            (>= (dc_door_perception ?perception ?location ?destination) (skill_check ?player ?perception))
        )
        :effect (and 
            (not (locked ?location ?destination))
            (not (locked ?destination ?location))
        )
    )

    ; An player breaks down a door
    (:action break_door
        :parameters (?player - player ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (connected ?location ?destination)
            (locked ?location ?destination)
            (<= (hp_door ?location ?destination) 0)
        )
        :effect (and 
            (not (locked ?location ?destination))
            (not (locked ?destination ?location))
        )
    )

    ; An player damages a door
    (:action damage_door
        :parameters (?player - player ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (connected ?location ?destination)
            (locked ?location ?destination)
            (> (hp_door ?location ?destination) 0)
            (> (attack_roll ?player) (ac_door ?location ?destination))
        )
        :effect (and 
            (decrease (hp_door ?location ?destination) (damage ?player))
            (decrease (hp_door ?destination ?location) (damage ?player))
        )
    )
)