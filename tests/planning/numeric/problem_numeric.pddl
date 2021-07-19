(define (problem fighter) (:domain dnd)
(:objects 
    ; Player
    player - player
    ; NPCs
    corvus - npc
    anvil - npc
    ; Rooms
    stout_meal_inn - room
    inns_cellar - room
    dungeon_entrance - room
    burial_chamber - room
    western_corridor - room
    antechamber - room
    southern_corridor - room
    baradins_crypt - room
    ; Monsters
    cat - cat
    giant_rat1 - giant_rat
    giant_rat2 - giant_rat
    giant_rat3 - giant_rat
    giant_rat4 - giant_rat
    goblin1 - goblin
    goblin2 - goblin
    goblin3 - goblin
    skeleton - skeleton
    zombie - zombie
    ; Abilities
    cha - ability
    con - ability
    dex - ability
    int - ability
    str - ability
    wis - ability
    ; Skills
    perception - skill
)

(:init
    (alive player)
    (alive cat)
    (alive giant_rat1)
    (alive giant_rat2)
    (alive giant_rat3)
    (alive giant_rat4)
    (alive goblin2)
    (alive goblin3)
    (alive skeleton)
    (alive zombie)
    (strength str)
    (perception perception)
    (at player stout_meal_inn)
    (at cat inns_cellar)
    (at giant_rat1 inns_cellar)
    (at giant_rat2 inns_cellar)
    (at giant_rat3 inns_cellar)
    (at giant_rat4 inns_cellar)
    (at goblin1 dungeon_entrance)
    (at goblin2 antechamber)
    (at goblin3 antechamber)
    (at zombie dungeon_entrance)
    (at skeleton burial_chamber)
    (connected stout_meal_inn inns_cellar)
    (connected inns_cellar stout_meal_inn)
    (connected inns_cellar dungeon_entrance)
    (connected dungeon_entrance inns_cellar)
    (connected dungeon_entrance burial_chamber)
    (connected dungeon_entrance western_corridor)
    (locked dungeon_entrance burial_chamber)
    (locked dungeon_entrance western_corridor)
    (connected burial_chamber dungeon_entrance)
    (locked burial_chamber dungeon_entrance)
    (connected western_corridor dungeon_entrance)
    (connected western_corridor antechamber)
    (locked western_corridor dungeon_entrance)
    (connected antechamber western_corridor)
    (connected antechamber southern_corridor)
    (locked antechamber southern_corridor)
    (connected southern_corridor antechamber)
    (connected southern_corridor baradins_crypt)
    (locked southern_corridor antechamber)
    (locked southern_corridor baradins_crypt)
    (connected baradins_crypt southern_corridor)
    (locked baradins_crypt southern_corridor)
    ; set DC for doors
    (= (dc_door_str str dungeon_entrance burial_chamber) 15)
    (= (dc_door_str str dungeon_entrance western_corridor) 15)
    (= (dc_door_str str burial_chamber dungeon_entrance) 15)
    (= (dc_door_str str western_corridor dungeon_entrance) 15)
    (= (dc_door_perception perception dungeon_entrance burial_chamber) 10)
    (= (dc_door_perception perception dungeon_entrance western_corridor) 10)
    (= (dc_door_perception perception burial_chamber dungeon_entrance) 10)
    (= (dc_door_perception perception western_corridor dungeon_entrance) 10)
    (= (dc_door_str str antechamber southern_corridor) 21)
    (= (dc_door_str str southern_corridor antechamber) 21)
    ; set HP for doors
    (= (hp_door dungeon_entrance burial_chamber) 27)
    (= (hp_door burial_chamber dungeon_entrance) 27)
    (= (hp_door dungeon_entrance western_corridor) 27)
    (= (hp_door western_corridor dungeon_entrance) 27)
    (= (hp_door antechamber southern_corridor) 39)
    (= (hp_door southern_corridor antechamber) 39)
    ; set AC for doors
    (= (ac_door dungeon_entrance burial_chamber) 19)
    (= (ac_door dungeon_entrance western_corridor) 19)
    (= (ac_door burial_chamber dungeon_entrance) 19)
    (= (ac_door western_corridor dungeon_entrance) 19)
    (= (ac_door antechamber southern_corridor) 19)
    (= (ac_door southern_corridor antechamber) 19)

    ; set ability check
    (= (ability_check player str) 20)
    ; set skill check
    (= (skill_check player perception) 20)
    ; set attack roll
    (= (attack_roll player) 20)
    ; set damage dealt
    (= (damage player) 10)
)

(:goal (and
    (at player southern_corridor
    )
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
