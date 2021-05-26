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
    storage_room - room
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
    (at goblin1 storage_room)
    (at goblin2 antechamber)
    (at goblin3 antechamber)
    (at zombie storage_room)
    (at skeleton burial_chamber)
    (connected stout_meal_inn inns_cellar)
    (connected inns_cellar stout_meal_inn)
    (connected inns_cellar storage_room)
    (connected storage_room inns_cellar)
    (connected storage_room burial_chamber)
    (connected storage_room western_corridor)
    (locked storage_room burial_chamber)
    (locked storage_room western_corridor)
    (connected burial_chamber storage_room)
    (locked burial_chamber storage_room)
    (connected western_corridor storage_room)
    (connected western_corridor antechamber)
    (locked western_corridor storage_room)
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
    (= (dc_door_str str storage_room burial_chamber) 15)
    (= (dc_door_str str storage_room western_corridor) 15)
    (= (dc_door_str str burial_chamber storage_room) 15)
    (= (dc_door_str str western_corridor storage_room) 15)
    (= (dc_door_perception perception storage_room burial_chamber) 10)
    (= (dc_door_perception perception storage_room western_corridor) 10)
    (= (dc_door_perception perception burial_chamber storage_room) 10)
    (= (dc_door_perception perception western_corridor storage_room) 10)
    (= (dc_door_str str antechamber southern_corridor) 21)
    (= (dc_door_str str southern_corridor antechamber) 21)
    ; set HP for doors
    (= (hp_door storage_room burial_chamber) 27)
    (= (hp_door burial_chamber storage_room) 27)
    (= (hp_door storage_room western_corridor) 27)
    (= (hp_door western_corridor storage_room) 27)
    (= (hp_door antechamber southern_corridor) 39)
    (= (hp_door southern_corridor antechamber) 39)
    ; set AC for doors
    (= (ac_door storage_room burial_chamber) 19)
    (= (ac_door storage_room western_corridor) 19)
    (= (ac_door burial_chamber storage_room) 19)
    (= (ac_door western_corridor storage_room) 19)
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
