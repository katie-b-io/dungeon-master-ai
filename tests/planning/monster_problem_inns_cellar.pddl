(define (problem inns_cellar) (:domain dnd_monster)

    (:objects 
        ; Monsters
        giant_rat1 - giant_rat
        giant_rat2 - giant_rat
        giant_rat3 - giant_rat
        giant_rat4 - diseased_giant_rat
        ; Player
        player - player
        ; Room
        inns_cellar - room
        ; Weapons
        bite - weapon
        claws - weapon
    )

    (:init
        ; =======================================
        ; Monster
        (alive giant_rat1)
        (alive giant_rat2)
        (alive giant_rat3)
        (alive giant_rat4)
        (at giant_rat1 inns_cellar)
        (at giant_rat2 inns_cellar)
        (at giant_rat3 inns_cellar)
        (at giant_rat4 inns_cellar)
        ; set weapons
        (has giant_rat1 bite)
        (has giant_rat1 claws)
        (has giant_rat2 bite)
        (has giant_rat2 claws)
        (has giant_rat3 bite)
        (has giant_rat3 claws)
        (has giant_rat4 bite)
        (has giant_rat4 claws)
        (equipped giant_rat1 bite)
        (equipped giant_rat1 claws)
        (equipped giant_rat2 bite)
        (equipped giant_rat2 claws)
        (equipped giant_rat3 bite)
        (equipped giant_rat3 claws)
        (equipped giant_rat4 bite)
        (equipped giant_rat4 claws)

        ; =======================================
        ; Player
        (alive player)
        (at player inns_cellar)

        ; =======================================
        ; Combat
        (must_kill player)
        (advantage giant_rat1 bite)
        (advantage giant_rat1 claws)
        (advantage giant_rat2 bite)
        (advantage giant_rat2 claws)
        (advantage giant_rat3 bite)
        (advantage giant_rat3 claws)
        (advantage giant_rat4 bite)
        (advantage giant_rat4 claws)
        (attacked player giant_rat1)
    )

    (:goal (and
        (or 
            (and
                (not (attacked player giant_rat1))
                (not (attacked player giant_rat2))
                (not (attacked player giant_rat3))
                (not (attacked player giant_rat4))
            )
            (and
                (not (alive player))
            )
        )
    ))
)
