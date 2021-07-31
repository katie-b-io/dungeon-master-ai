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
        corridor_1 - room
        inns_cellar - room
        corridor_2 - room
        dungeon_entrance - room
        corridor_3 - room
        burial_chamber - room
        corridor_4 - room
        western_corridor - room
        corridor_5 - room
        antechamber - room
        corridor_6 - room
        southern_corridor - room
        corridor_7 - room
        baradins_crypt - room

        stout_meal_inn---corridor_1 - door
        corridor_1---inns_cellar - door

        inns_cellar---corridor_2 - door
        corridor_2---dungeon_entrance - door

        dungeon_entrance---corridor_3 - door
        corridor_3---burial_chamber - door

        dungeon_entrance---corridor_4 - door
        corridor_4---western_corridor - door

        western_corridor---corridor_5 - door
        corridor_5---antechamber - door

        antechamber---corridor_6 - door
        corridor_6---southern_corridor - door

        southern_corridor---corridor_7 - door
        corridor_7---baradins_crypt - door

        giant_rat_1 - giant_rat
        giant_rat_2 - giant_rat
        zombie_1 - zombie
        goblin_1 - goblin
        skeleton_1 - skeleton
        goblin_2 - goblin
        goblin_3 - goblin

        additional_zombie_1 - zombie
        additional_zombie_2 - zombie
        additional_zombie_3 - zombie
        additional_zombie_4 - zombie
        additional_giant_rat_1 - giant_rat
        additional_giant_rat_2 - giant_rat
        additional_giant_rat_3 - giant_rat
        additional_giant_rat_4 - giant_rat
        additional_skeleton_1 - skeleton
        additional_skeleton_2 - skeleton
        additional_skeleton_3 - skeleton
        additional_skeleton_4 - skeleton
        additional_goblin_1 - goblin
        additional_goblin_2 - goblin

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
        (injured player)
        (torch_lit)
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
        (at anvil stout_meal_inn)
        (alive anvil)
        (improve_attitude indifferent friendly)
        (improve_attitude hostile indifferent)
        (degrade_attitude friendly indifferent)
        (degrade_attitude indifferent hostile)
        (attitude_towards_player corvus friendly)
        (attitude_towards_player anvil indifferent)
        (at giant_rat_1 inns_cellar)
        (at giant_rat_2 inns_cellar)
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
        (must_kill zombie_1)
        (must_kill goblin_2)
        (must_kill goblin_3)
        (dark inns_cellar)

        (alive additional_zombie_1)
        (must_kill additional_zombie_1)
        (at additional_zombie_1 corridor_1)
        (alive additional_zombie_3)
        (must_kill additional_zombie_3)
        (at additional_zombie_3 corridor_1)
        (alive additional_zombie_2)
        (must_kill additional_zombie_2)
        (at additional_zombie_2 corridor_2)
        (alive additional_zombie_4)
        (must_kill additional_zombie_4)
        (at additional_zombie_4 corridor_2)
        (alive additional_giant_rat_1)
        (must_kill additional_giant_rat_1)
        (at additional_giant_rat_1 corridor_3)
        (alive additional_giant_rat_3)
        (must_kill additional_giant_rat_3)
        (at additional_giant_rat_3 corridor_3)
        (alive additional_giant_rat_2)
        (must_kill additional_giant_rat_2)
        (at additional_giant_rat_2 corridor_4)
        (alive additional_giant_rat_4)
        (must_kill additional_giant_rat_4)
        (at additional_giant_rat_4 corridor_4)
        (alive additional_skeleton_1)
        (must_kill additional_skeleton_1)
        (at additional_skeleton_1 corridor_5)
        (alive additional_skeleton_3)
        (must_kill additional_skeleton_3)
        (at additional_skeleton_3 corridor_5)
        (alive additional_skeleton_2)
        (must_kill additional_skeleton_2)
        (at additional_skeleton_2 corridor_6)
        (alive additional_skeleton_4)
        (must_kill additional_skeleton_4)
        (at additional_skeleton_4 corridor_6)
        (alive additional_goblin_1)
        (must_kill additional_goblin_1)
        (at additional_goblin_1 corridor_7)
        (alive additional_goblin_2)
        (must_kill additional_goblin_2)
        (at additional_goblin_2 corridor_7)

        (treasure inns_cellar)
        (treasure corridor_1)
        (treasure corridor_2)
        (treasure corridor_3)
        (treasure corridor_4)
        (treasure corridor_5)
        (treasure corridor_6)
        (treasure corridor_7)
        (dark dungeon_entrance)
        (dark burial_chamber)
        (dark western_corridor)
        (dark southern_corridor)
        (dark baradins_crypt)
        
        (connected stout_meal_inn---corridor_1 stout_meal_inn corridor_1)
        (connected stout_meal_inn---corridor_1 corridor_1 stout_meal_inn)
        (at stout_meal_inn---corridor_1 stout_meal_inn)
        (at stout_meal_inn---corridor_1 corridor_1)
        (alive stout_meal_inn---corridor_1)

        (connected corridor_1---inns_cellar corridor_1 inns_cellar)
        (connected corridor_1---inns_cellar inns_cellar corridor_1)
        (at corridor_1---inns_cellar corridor_1)
        (at corridor_1---inns_cellar inns_cellar)
        (locked corridor_1---inns_cellar)
        (alive corridor_1---inns_cellar)

        (connected inns_cellar---corridor_2 inns_cellar corridor_2)
        (connected inns_cellar---corridor_2 corridor_2 inns_cellar)
        (at inns_cellar---corridor_2 inns_cellar)
        (at inns_cellar---corridor_2 corridor_2)
        (alive inns_cellar---corridor_2)

        (connected corridor_2---dungeon_entrance corridor_2 dungeon_entrance)
        (connected corridor_2---dungeon_entrance dungeon_entrance corridor_2)
        (at corridor_2---dungeon_entrance corridor_2)
        (at corridor_2---dungeon_entrance dungeon_entrance)
        (locked corridor_2---dungeon_entrance)
        (alive corridor_2---dungeon_entrance)

        (connected dungeon_entrance---corridor_3 dungeon_entrance corridor_3)
        (connected dungeon_entrance---corridor_3 corridor_3 dungeon_entrance)
        (at dungeon_entrance---corridor_3 dungeon_entrance)
        (at dungeon_entrance---corridor_3 corridor_3)
        (alive dungeon_entrance---corridor_3)

        (connected corridor_3---burial_chamber corridor_3 burial_chamber)
        (connected corridor_3---burial_chamber burial_chamber corridor_3)
        (at corridor_3---burial_chamber corridor_3)
        (at corridor_3---burial_chamber burial_chamber)
        (locked corridor_3---burial_chamber)
        (alive corridor_3---burial_chamber)

        (connected dungeon_entrance---corridor_4 dungeon_entrance corridor_4)
        (connected dungeon_entrance---corridor_4 corridor_4 dungeon_entrance)
        (at dungeon_entrance---corridor_4 dungeon_entrance)
        (at dungeon_entrance---corridor_4 corridor_4)
        (alive dungeon_entrance---corridor_4)

        (connected corridor_4---western_corridor corridor_4 western_corridor)
        (connected corridor_4---western_corridor western_corridor corridor_4)
        (at corridor_4---western_corridor corridor_4)
        (at corridor_4---western_corridor western_corridor)
        (locked corridor_4---western_corridor)
        (alive corridor_4---western_corridor)

        (connected western_corridor---corridor_5 western_corridor corridor_5)
        (connected western_corridor---corridor_5 corridor_5 western_corridor)
        (at western_corridor---corridor_5 western_corridor)
        (at western_corridor---corridor_5 corridor_5)
        (alive western_corridor---corridor_5)

        (connected corridor_5---antechamber corridor_5 antechamber)
        (connected corridor_5---antechamber antechamber corridor_5)
        (at corridor_5---antechamber corridor_5)
        (at corridor_5---antechamber antechamber)
        (locked corridor_5---antechamber)
        (alive corridor_5---antechamber)

        (connected antechamber---corridor_6 antechamber corridor_6)
        (connected antechamber---corridor_6 corridor_6 antechamber)
        (at antechamber---corridor_6 antechamber)
        (at antechamber---corridor_6 corridor_6)
        (alive antechamber---corridor_6)

        (connected corridor_6---southern_corridor corridor_6 southern_corridor)
        (connected corridor_6---southern_corridor southern_corridor corridor_6)
        (at corridor_6---southern_corridor corridor_6)
        (at corridor_6---southern_corridor southern_corridor)
        (locked corridor_6---southern_corridor)
        (alive corridor_6---southern_corridor)

        (connected southern_corridor---corridor_7 southern_corridor corridor_7)
        (connected southern_corridor---corridor_7 corridor_7 southern_corridor)
        (at southern_corridor---corridor_7 southern_corridor)
        (at southern_corridor---corridor_7 corridor_7)
        (alive southern_corridor---corridor_7)

        (connected corridor_7---baradins_crypt corridor_7 baradins_crypt)
        (connected corridor_7---baradins_crypt baradins_crypt corridor_7)
        (at corridor_7---baradins_crypt corridor_7)
        (at corridor_7---baradins_crypt baradins_crypt)
        (locked corridor_7---baradins_crypt)
        (alive corridor_7---baradins_crypt)

        (potion_of_healing potion_of_healing)
        (wand_of_magic_missiles wand_of_magic_missiles)
        (dwarven_thrower dwarven_thrower)
        (silver_key silver_key)
        (at silver_key burial_chamber)
        (bronze_key bronze_key)
        (has player bronze_key)
        (explore_solution corridor_4---western_corridor)
        (at vault_puzzle burial_chamber)
        (at silver_key_puzzle burial_chamber)
        (explore_solution silver_key_puzzle)
        (at skull_engraving_puzzle burial_chamber)
        (at altar_puzzle burial_chamber)

        (ability_solution corridor_1---inns_cellar str)
        (intent_solution corridor_2---dungeon_entrance attack_intent)
        (explore_solution corridor_3---burial_chamber)
        (intent_solution corridor_5---antechamber attack_intent)
        
        (ability_solution corridor_6---southern_corridor str)
        (item_solution corridor_7---baradins_crypt bronze_key)
        (at dwarven_thrower_puzzle baradins_crypt)
        (explore_solution dwarven_thrower_puzzle)
    )

    (:goal
        (and
            (has player dwarven_thrower_puzzle)
        )
    )
)
