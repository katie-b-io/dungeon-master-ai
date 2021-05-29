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
    ; Doors
    door1 - door
    door2 - door
    door3 - door
    door4 - door
    door5 - door
    door6 - door
    door7 - door
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
    ; Equipment
    thieves_tools - equipment
)

(:init
    ; =======================================
    ; Player
    (alive player)
    (at player stout_meal_inn)
    ; set abilities
    (charisma cha)
    (constitution con)
    (dexterity dex)
    (intelligence int)
    (strength str)
    (wisdom wis)
    ; set skills
    (perception perception)
    ; set equipment
    (thieves_tools thieves_tools)

    ; =======================================
    ; Monsters
    (alive cat)
    (alive giant_rat1)
    (alive giant_rat2)
    (alive giant_rat3)
    (alive giant_rat4)
    (alive goblin2)
    (alive goblin3)
    (alive skeleton)
    (alive zombie)
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

    ; =======================================
    ; Rooms
    (connected door1 stout_meal_inn inns_cellar)
    (connected door1 inns_cellar stout_meal_inn)
    (connected door2 inns_cellar storage_room)
    (connected door2 storage_room stout_meal_inn)
    (connected door3 storage_room burial_chamber)
    (connected door3 burial_chamber storage_room)
    (connected door4 storage_room western_corridor)
    (connected door4 western_corridor storage_room)
    (connected door5 western_corridor antechamber)
    (connected door5 antechamber western_corridor)
    (connected door6 antechamber southern_corridor)
    (connected door6 southern_corridor antechamber)
    (connected door7 southern_corridor baradins_crypt)
    (connected door7 baradins_crypt southern_corridor)
    (at door1 stout_meal_inn)
    (at door1 inns_cellar)
    (at door2 inns_cellar)
    (at door2 storage_room)
    (at door3 storage_room)
    (at door3 burial_chamber)
    (at door4 storage_room)
    (at door4 western_corridor)
    (at door5 western_corridor)
    (at door5 antechamber)
    (at door6 antechamber)
    (at door6 southern_corridor)
    (at door7 southern_corridor)
    (at door7 baradins_crypt)
    (locked door3)
    (locked door4)
    (locked door6)
    (locked door7)

    ; =======================================
    ; Challenges
    ; set DC for doors
    (dc door3 str)
    (dc door4 str)
    (dc door6 str)
    (dc door3 perception)
    (dc door4 perception)
    ; set equipment DC for doors
    (dc_equipment door6 thieves_tools)
    ; set HP for doors
    (hp door3)
    (hp door4)
    (hp door6)
    ; set AC for doors
    (ac door3)
    (ac door4)
    (ac door6)

)

(:goal (and
    (at player southern_corridor)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
