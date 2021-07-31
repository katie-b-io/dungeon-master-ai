(define (problem fighter) (:domain player)

    (:objects
        player - player
        no_intent_intent - intent
        hint_intent - intent
        move_intent - intent
        attack_intent - intent
        use_intent - intent
        stop_using_intent - intent
        equip_intent - intent
        unequip_intent - intent
        converse_intent - intent
        affirm_intent - intent
        deny_intent - intent
        explore_intent - intent
        roll_intent - intent
        pick_up_intent - intent
        health_intent - intent
        inventory_intent - intent
        force_intent - intent
        ability_check_intent - intent
        skill_check_intent - intent
        ale_intent - intent
        roleplay_intent - intent
        negotiate_intent - intent
        rescue_intent - intent
        bot_challenge_intent - intent
        stealth_intent - intent
        pick_lock_intent - intent
        potion_of_healing - item
        wand_of_magic_missiles - item
        dwarven_thrower - item
        silver_key - item
        bronze_key - item
        corvus - npc
        anvil - npc
        indifferent - indifferent
        friendly - friendly
        hostile - hostile
        stout_meal_inn - room
        inns_cellar - room
        dungeon_entrance - room
        burial_chamber - room
        western_corridor - room
        antechamber - room
        southern_corridor - room
        baradins_crypt - room
        stout_meal_inn---inns_cellar - door
        inns_cellar---dungeon_entrance - door
        dungeon_entrance---burial_chamber - door
        dungeon_entrance---western_corridor - door
        western_corridor---antechamber - door
        antechamber---southern_corridor - door
        southern_corridor---baradins_crypt - door
        giant_rat_1 - giant_rat
        giant_rat_2 - giant_rat
        giant_rat_3 - giant_rat
        giant_rat_4 - giant_rat
        giant_rat_5 - giant_rat
        giant_rat_6 - giant_rat
        giant_rat_7 - giant_rat
        giant_rat_8 - giant_rat
        zombie_1 - zombie
        goblin_1 - goblin
        skeleton_1 - skeleton
        goblin_2 - goblin
        goblin_3 - goblin
        str - ability
        dex - ability
        con - ability
        int - ability
        wis - ability
        cha - ability
        acrobatics - skill
        animal_handling - skill
        arcana - skill
        athletics - skill
        deception - skill
        history - skill
        insight - skill
        intimidation - skill
        investigation - skill
        medicine - skill
        nature - skill
        perception - skill
        performance - skill
        persuasion - skill
        religion - skill
        sleight_of_hand - skill
        stealth - skill
        survival - skill
        greataxe - weapon
        backpack - equipment
        bedroll - equipment
        bolts - equipment
        mess_kit - equipment
        rations - equipment
        rope_hempen - equipment
        set_of_common_clothes - equipment
        tinder_box - equipment
        torch - equipment
        waterskin - equipment
        vault_puzzle - puzzle
        silver_key_puzzle - puzzle
        skull_engraving_puzzle - puzzle
        altar_puzzle - puzzle
        dwarven_thrower_puzzle - puzzle
    )

    (:init
        (quest)
        (at player stout_meal_inn)
        (alive player)
        (strength str)
        (dexterity dex)
        (constitution con)
        (intelligence int)
        (wisdom wis)
        (charisma cha)
        (acrobatics acrobatics)
        (animal_handling animal_handling)
        (arcana arcana)
        (athletics athletics)
        (deception deception)
        (history history)
        (insight insight)
        (intimidation intimidation)
        (investigation investigation)
        (medicine medicine)
        (nature nature)
        (perception perception)
        (performance performance)
        (persuasion persuasion)
        (religion religion)
        (sleight_of_hand sleight_of_hand)
        (stealth stealth)
        (survival survival)
        (has player greataxe)
        (equipped player greataxe)
        (backpack backpack)
        (has player backpack)
        (bedroll bedroll)
        (has player bedroll)
        (bolts bolts)
        (has player bolts)
        (mess_kit mess_kit)
        (has player mess_kit)
        (rations rations)
        (has player rations)
        (rope_hempen rope_hempen)
        (has player rope_hempen)
        (set_of_common_clothes set_of_common_clothes)
        (has player set_of_common_clothes)
        (tinder_box tinder_box)
        (has player tinder_box)
        (torch torch)
        (has player torch)
        (waterskin waterskin)
        (has player waterskin)
        (at corvus stout_meal_inn)
        (alive corvus)
        (gives_quest corvus)
        (at anvil inns_cellar)
        (alive anvil)
        (improve_attitude indifferent friendly)
        (improve_attitude hostile indifferent)
        (degrade_attitude friendly indifferent)
        (degrade_attitude indifferent hostile)
        (attitude_towards_player corvus friendly)
        (attitude_towards_player anvil indifferent)
        (at giant_rat_1 inns_cellar)
        (alive giant_rat_1)
        (at giant_rat_2 inns_cellar)
        (alive giant_rat_2)
        (at giant_rat_3 inns_cellar)
        (alive giant_rat_3)
        (at giant_rat_4 inns_cellar)
        (alive giant_rat_4)
        (at giant_rat_5 inns_cellar)
        (alive giant_rat_5)
        (at giant_rat_6 inns_cellar)
        (alive giant_rat_6)
        (at giant_rat_7 inns_cellar)
        (alive giant_rat_7)
        (at giant_rat_8 inns_cellar)
        (alive giant_rat_8)
        (at zombie_1 dungeon_entrance)
        (alive zombie_1)
        (at goblin_1 dungeon_entrance)
        (treasure goblin_1)
        (at skeleton_1 burial_chamber)
        (at goblin_2 antechamber)
        (alive goblin_2)
        (at goblin_3 antechamber)
        (alive goblin_3)
        (must_kill giant_rat_1)
        (must_kill giant_rat_2)
        (must_kill giant_rat_3)
        (must_kill giant_rat_4)
        (must_kill giant_rat_5)
        (must_kill giant_rat_6)
        (must_kill giant_rat_7)
        (must_kill giant_rat_8)
        (must_kill zombie_1)
        (must_kill goblin_2)
        (must_kill goblin_3)
        (dark inns_cellar)
        (treasure inns_cellar)
        (dark dungeon_entrance)
        (dark burial_chamber)
        (dark western_corridor)
        (dark southern_corridor)
        (dark baradins_crypt)
        (connected stout_meal_inn---inns_cellar stout_meal_inn inns_cellar)
        (connected stout_meal_inn---inns_cellar inns_cellar stout_meal_inn)
        (at stout_meal_inn---inns_cellar stout_meal_inn)
        (at stout_meal_inn---inns_cellar inns_cellar)
        (alive stout_meal_inn---inns_cellar)
        (connected inns_cellar---dungeon_entrance inns_cellar dungeon_entrance)
        (connected inns_cellar---dungeon_entrance dungeon_entrance inns_cellar)
        (at inns_cellar---dungeon_entrance inns_cellar)
        (at inns_cellar---dungeon_entrance dungeon_entrance)
        (alive inns_cellar---dungeon_entrance)
        (connected dungeon_entrance---burial_chamber dungeon_entrance burial_chamber)
        (connected dungeon_entrance---burial_chamber burial_chamber dungeon_entrance)
        (at dungeon_entrance---burial_chamber dungeon_entrance)
        (at dungeon_entrance---burial_chamber burial_chamber)
        (alive dungeon_entrance---burial_chamber)
        (connected dungeon_entrance---western_corridor dungeon_entrance western_corridor)
        (connected dungeon_entrance---western_corridor western_corridor dungeon_entrance)
        (at dungeon_entrance---western_corridor dungeon_entrance)
        (at dungeon_entrance---western_corridor western_corridor)
        (locked dungeon_entrance---western_corridor)
        (alive dungeon_entrance---western_corridor)
        (connected western_corridor---antechamber western_corridor antechamber)
        (connected western_corridor---antechamber antechamber western_corridor)
        (at western_corridor---antechamber western_corridor)
        (at western_corridor---antechamber antechamber)
        (alive western_corridor---antechamber)
        (connected antechamber---southern_corridor antechamber southern_corridor)
        (connected antechamber---southern_corridor southern_corridor antechamber)
        (at antechamber---southern_corridor antechamber)
        (at antechamber---southern_corridor southern_corridor)
        (locked antechamber---southern_corridor)
        (alive antechamber---southern_corridor)
        (connected southern_corridor---baradins_crypt southern_corridor baradins_crypt)
        (connected southern_corridor---baradins_crypt baradins_crypt southern_corridor)
        (at southern_corridor---baradins_crypt southern_corridor)
        (at southern_corridor---baradins_crypt baradins_crypt)
        (locked southern_corridor---baradins_crypt)
        (alive southern_corridor---baradins_crypt)
        (potion_of_healing potion_of_healing)
        (wand_of_magic_missiles wand_of_magic_missiles)
        (dwarven_thrower dwarven_thrower)
        (silver_key silver_key)
        (at silver_key burial_chamber)
        (bronze_key bronze_key)
        (has corvus bronze_key)
        (explore_solution dungeon_entrance---western_corridor)
        (at vault_puzzle burial_chamber)
        (at silver_key_puzzle burial_chamber)
        (explore_solution silver_key_puzzle)
        (at skull_engraving_puzzle burial_chamber)
        (at altar_puzzle burial_chamber)
        (ability_solution antechamber---southern_corridor str)
        (at dwarven_thrower_puzzle baradins_crypt)
        (explore_solution dwarven_thrower_puzzle)
    )

    (:goal
        (and
            (not (alive giant_rat_1))
            (not (alive giant_rat_2))
            (not (alive giant_rat_3))
            (not (alive giant_rat_4))
            (not (alive giant_rat_5))
            (not (alive giant_rat_6))
            (not (alive giant_rat_7))
            (not (alive giant_rat_8))
            (at player stout_meal_inn)
        )
    )
)

