(define (problem inns_cellar) (:domain dnd_monster)

    (:objects 
        ; Monsters
        giant_rat1 - giant_rat
        ; Player
        player - player
        ; Room
        inns_cellar - room
        ; Weapons
        bite - weapon
    )

    (:init
        ; =======================================
        ; Monster
        (alive giant_rat1)
        (at giant_rat1 inns_cellar)
        ; set weapons
        (has giant_rat1 bite)
        (equipped giant_rat1 bite)
        ; Visibility
        (dark inns_cellar)
        (darkvision)

        ; =======================================
        ; Player
        (alive player)
        (at player inns_cellar)

        ; =======================================
        ; Combat
        (must_kill player)
        (advantage giant_rat1 bite)
    )

    (:goal (and
        (or 
            (and
                (not (must_kill player))
                (not (attacked player giant_rat1))
            )
            (and
                (not (alive player))
            )
        )
    ))
)
