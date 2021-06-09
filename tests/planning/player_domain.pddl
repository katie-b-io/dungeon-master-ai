;Dungeons and Dragons 5th Edition Domain

(define (domain dnd_player)

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
        ; Roleplaying exists
        attitude - object
        neutral positive negative - attitude
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
        ; DC of object
        (dc ?target - object ?ability - ability)
        (dc_equipment ?target - object ?equipment - equipment)
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
        ; Tools
        (thieves_tools ?equipment - equipment)
        ; Action is performed
        (action)
        ; NPC attitudes
        (attitude_towards_player ?npc - npc ?attitude - attitude)
        (improve_attitude ?current - attitude ?next - attitude)
        (degrade_attitude ?current - attitude ?next - attitude)
        ; Combat
        (combat)
        (must_kill ?monster - monster)
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
        :parameters (?player - player ?npc - npc ?positive - positive ?location - room)
        :precondition (and
            (alive ?player)
            (alive ?npc)
            (at ?player ?location)
            (at ?npc ?location)
            (gives_quest ?npc)
            (attitude_towards_player ?npc ?positive)
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