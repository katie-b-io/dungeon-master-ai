;Dungeons and Dragons 5th Edition Domain

(define (domain dnd_monster)

    (:requirements 
        :strips
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
        ranged_weapon - weapon
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
        ; Visibility
        (torch_lit)
        (darkvision)
        (dark ?room - room)
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
            (can_damage_roll ?monster ?target)
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
            (can_damage_roll ?monster ?target)
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
            (can_damage_roll ?monster ?target)
        )
    )

    ; Monster damages a target
    (:action damage_roll
        :parameters (?monster - monster ?weapon - weapon ?target - object ?location - room)
        :precondition (and 
            (at ?monster ?location)
            (at ?target ?location)
            (can_damage_roll ?monster ?target)
            (alive ?target)
            (higher_than_ac ?target)
            (equipped ?monster ?weapon)
        )
        :effect (and 
            (not (can_damage_roll ?monster ?target))
            (not (higher_than_ac ?target))
            (damaged ?target)
            (not (attack_roll_success ?monster ?target))
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
            (or
                (not (dark ?location))
                (or (torch_lit) (darkvision))
            )
        )
        :effect (and 
            (can_attack_roll ?monster ?target)
            (action)
            (combat)
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