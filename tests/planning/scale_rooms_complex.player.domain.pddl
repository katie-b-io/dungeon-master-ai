(define (domain player)

    (:requirements 
        :strips
        :typing
        :conditional-effects
        :negative-preconditions
        :equality
        :disjunctive-preconditions
    )

    (:types
        entity intent puzzle attitude ability room door weapon equipment item - object
        player npc monster - entity
        cat giant_rat goblin skeleton zombie - monster
        indifferent friendly hostile - attitude
        skill - ability
        ranged_weapon - weapon
    )

    (:predicates
        (quest)
        (complete)
        (gives_quest ?npc - npc)
        (treasure ?object - object)
        (advantage ?object - object)
        (disadvantage ?object - object)
        (strength ?ability - ability)
        (dexterity ?ability - ability)
        (constitution ?ability - ability)
        (intelligence ?ability - ability)
        (wisdom ?ability - ability)
        (charisma ?ability - ability)
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
        (has ?entity - entity ?object - object)
        (at ?object - object ?room - room)
        (alive ?object - object)
        (injured ?player - player)
        (damaged ?object - object)
        (equipped ?player - player ?object - object)
        (connected ?door - door ?location - room ?destination - room)
        (locked ?door - door)
        (higher_than_ac ?target - object)
        (can_attack_roll ?player - player ?target - object)
        (can_damage_roll ?player - player ?target - object)
        (can_ability_check ?player - player ?ability - ability ?target - object)
        (can_equipment_check ?player - player ?equipment - equipment ?target - object)
        (ability_check_success ?player - player ?ability - ability ?target - object)
        (equipment_check_success ?player - player ?equipment - equipment ?target - object)
        (attack_roll_success ?player - player ?target - object)
        (backpack ?equipment - equipment)
        (bedroll ?equipment - equipment)
        (bolts ?equipment - equipment)
        (mess_kit ?equipment - equipment)
        (rations ?equipment - equipment)
        (rope_hempen ?equipment - equipment)
        (set_of_common_clothes ?equipment - equipment)
        (tinder_box ?equipment - equipment)
        (torch ?equipment - equipment)
        (waterskin ?equipment - equipment)
        (potion_of_healing ?item - item)
        (wand_of_magic_missiles ?item - item)
        (dwarven_thrower ?item - item)
        (silver_key ?item - item)
        (bronze_key ?item - item)
        (action)
        (torch_lit)
        (darkvision)
        (dark ?room - room)
        (attitude_towards_player ?npc - npc ?attitude - attitude)
        (improve_attitude ?current - attitude ?next - attitude)
        (degrade_attitude ?current - attitude ?next - attitude)
        (combat)
        (must_kill ?monster - monster)
        (explore_solution ?target - object)
        (ability_solution ?target - object ?ability - ability)
        (equipment_solution ?target - object ?equipment - equipment)
        (intent_solution ?target - object ?intent - intent)
        (item_solution ?target - object ?item - item)
    )

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
    )

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
    )

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
    )

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
    )

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
    )

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
    )

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
    )

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
    )

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
    )

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
    )

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
    )

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
    )

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
    )

    ; Player investigates puzzle
    (:action investigate_puzzle
        :parameters (?player - player ?location - room ?puzzle - puzzle)
        :precondition (and 
            (at ?player ?location)
            (at ?puzzle ?location)
            (not (has ?player ?puzzle))
            (explore_solution ?puzzle)
        )
        :effect (and 
            (has ?player ?puzzle)
        )
    )

    ; Player investigates monster
    (:action investigate_monster
        :parameters (?player - player ?location - room ?monster - monster)
        :precondition (and 
            (at ?player ?location)
            (at ?monster ?location)
            (treasure ?monster)
            (not (alive ?monster))
        )
        :effect (and 
            (not (treasure ?monster))
        )
    )

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
    )

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
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
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
                        (not (treasure ?monster))
                    )
                    (and 
                        (at ?monster ?location)
                        (must_kill ?monster)
                        (not (alive ?monster))
                        (not (treasure ?monster))
                    )
                )
            )
        )
        :effect (and 
            (not (at ?player ?location))
            (at ?player ?destination)
        )
    )

    ; Player wants to open a door with an item
    (:action open_door_with_item
        :parameters (?player - player ?item - item ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (item_solution ?door ?item)
            (has ?player ?item)
            (not (action))
            (or
                (not (dark ?location))
                (or (torch_lit) (darkvision))
            )
            (or
                (not (injured ?player))
                (and
                    (injured ?player)
                    (forall (?item2 - item2)
                        (or
                            (not (potion_of_healing ?item2))
                            (and
                                (potion_of_healing ?item2)
                                (not (has ?player ?item2))
                            )
                        )
                    )
                )
            )
        )
        :effect (and 
            (not (locked ?door))
            (not (has ?player ?item))
        )
    )

    ; Player wants to open a door by exploring
    (:action open_door_with_explore
        :parameters (?player - player ?door - door ?location - room ?destination - room)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (explore_solution ?door)
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
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
                        )
                    )
                )
            )
        )
        :effect (and 
            (not (locked ?door))
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
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
                        )
                    )
                )
            )
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
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
                        )
                    )
                )
            )
        )
        :effect (and 
            (can_equipment_check ?player ?equipment ?door)
            (action)
        )
    )

    ; Player wants to open a door with attack
    (:action open_door_with_attack
        :parameters (?player - player ?door - door ?location - room ?destination - room ?intent - intent)
        :precondition (and 
            (alive ?player)
            (at ?player ?location)
            (at ?door ?location)
            (connected ?door ?location ?destination)
            (locked ?door)
            (intent_solution ?door ?intent)
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
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
                        )
                    )
                )
            )
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
            (or
                (not (dark ?location))
                (or (torch_lit) (darkvision))
            )
            (or
                (not (injured ?player))
                (and
                    (injured ?player)
                    (forall (?item - item)
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
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
            (or
                (not (dark ?location))
                (or (torch_lit) (darkvision))
            )
            (or
                (not (injured ?player))
                (and
                    (injured ?player)
                    (forall (?item - item)
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
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
            (or
                (not (dark ?location))
                (or (torch_lit) (darkvision))
            )
            (or
                (not (injured ?player))
                (and
                    (injured ?player)
                    (forall (?item - item)
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
                        )
                    )
                )
            )
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
            (or
                (not (dark ?location))
                (or (torch_lit) (darkvision))
            )
            (or
                (not (injured ?player))
                (and
                    (injured ?player)
                    (forall (?item - item)
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
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
    )

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
                        (or
                            (not (potion_of_healing ?item))
                            (and
                                (potion_of_healing ?item)
                                (not (has ?player ?item))
                            )
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

    ; Player lights a torch
    (:action light_torch
        :parameters (?player - player ?torch - equipment ?location - room)
        :precondition (and 
            (alive ?player)
            (torch ?torch)
            (has ?player ?torch)
            (at ?player ?location)
            (dark ?location)
        )
        :effect (and
            (torch_lit)
        )
    )

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
    )
)
