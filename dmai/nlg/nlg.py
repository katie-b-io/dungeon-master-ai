import random

from dmai.utils.text import Text


class NLGMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs) -> None:
        """NLG static singleton metaclass"""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class NLG(metaclass=NLGMeta):

    # class variable
    game = None

    def __init__(self) -> None:
        """NLG static class"""
        pass

    ############################################################
    # Player interaction utterances
    @classmethod
    def get_char_class(cls, characters: str) -> str:
        """Return utterance for character selection"""
        utters = [
            "Which character class would you like to play?\n{c}".format(
                c=characters),
            "Select a character class you like the sound of:\n{c}".format(
                c=characters),
            "Select a character class from the following choices:\n{c}".format(
                c=characters),
        ]
        return random.choice(utters)

    @classmethod
    def roll_reaction(cls, result: int) -> str:
        """Return utterance for reacting to a dice roll"""
        if result < 1:
            utters = [
                "Ouch!",
                "That is painful",
                "How unfortunate",
                "Oof"
            ]
        elif result > 19:
            utters = [
                "Nice!",
                "Truly magnificent",
                "Natural 20, way to go!",
                "That's how you do it!",
            ]
        else:
            utters = ["Well, it's a number!"]
        return random.choice(utters)
    
    @classmethod
    def get_player_name(cls, character_class: str, player_selected_class: bool = True) -> str:
        """Return the utterance for getting player's name"""
        if not player_selected_class:
            utters = [
                "You'll be playing as a {c}. What is your character's name?".format(c=character_class)
            ]
        else:
            utters = [
                "What is your character's name, this great {c}?".format(c=character_class),
                "Ahh, a {c}. Excellent choice! And what is your character's name?".
                format(c=character_class),
                "A {c}, marvelous! And what do they call your character?".format(
                    c=character_class),
            ]
        return random.choice(utters)

    @classmethod
    def get_action(cls, name: str) -> str:
        """Return the utterance for getting a player action"""
        utters = ["{n}, what do you do?".format(n=name)]
        return random.choice(utters)

    @classmethod
    def get_title(cls, title: str) -> str:
        """Return the utterance for introducing the adventure title"""
        utters = [
            "Welcome adventurer, today we're going to play {t}! Let me set the scene..."
            .format(t=title),
            "Today we'll play {t}, an exciting tale of adventure! Let me set the scene..."
            .format(t=title),
            "The title of the adventure we're about to play is: {t}. Let me set the scene..."
            .format(t=title),
        ]
        return random.choice(utters)

    @classmethod
    def acknowledge_name(cls, name: str) -> str:
        """Return the utterance for acknowledging player's name"""
        utters = [
            "{n}, simply majestic!".format(n=name),
            "{n}, the finest name in all the lands!".format(n=name),
            "{n}, that's a good one!".format(n=name),
        ]
        return random.choice(utters)

    ############################################################
    # Action utterances
    @classmethod
    def health_update(cls, current_hp, hp_max: int = None) -> str:
        """Return the utterance updating player about their current hp"""
        if not hp_max:
            m = ""
        else:
            m = " out of a maximum of {h} hp".format(h=hp_max)
        utters = [
            "You've got {h} hp left{m}.".format(h=current_hp, m=m)
        ]
        return random.choice(utters)
    
    @classmethod
    def heal(cls, hp, new_hp, character_class: str) -> str:
        """Return the utterance for healing by a given amount"""
        if hp <= 0:
            utters = [
                "Is this thing on? You didn't heal any hp! You've got {n} hp in total.".format(n=new_hp),
                "You healed a grand total of zero... zero hp?! You've got {n} hp in total.".format(n=new_hp),
                "That was completely ineffectual. You've still got {n} hp in total.".format(n=new_hp)
            ]
        elif (hp/new_hp) < 0.25:
            utters = [
                "You feel a modest surge of wellness as you heal {h} hp and you've got {n} hp in total.".format(n=new_hp, h=hp),
                "You feel a slight tingle in your chest as you heal {h} hp and you've got {n} hp in total.".format(n=new_hp, h=hp),
                "That was nice! You healed {h} hp and you've got {n} hp in total.".format(n=new_hp, h=hp),
            ]
        elif (hp/new_hp) < 0.5:
            utters = [
                "Ahh, that was refreshing! You healed {h} hp and you've got {n} hp in total.".format(n=new_hp, h=hp, c=character_class),
                "The healing rush hits you with {h} hp and you've got {n} hp in total.".format(n=new_hp, h=hp),
                "You feel reinvigorated! You healed {h} hp and you've got {n} hp in total.".format(n=new_hp, h=hp),
            ]
        else:
            utters = [
                "You feel like a new {c}! You healed {h} hp and you've got {n} hp in total.".format(n=new_hp, h=hp, c=character_class),
                "That felt amazing! You healed {h} hp and you've got {n} hp in total.".format(n=new_hp, h=hp),
                "You feel invincible! You healed {h} hp and you've got {n} hp in total.".format(n=new_hp, h=hp),
            ]
        return random.choice(utters)
    
    @classmethod
    def pick_up(cls, item: str) -> str:
        """Return the utterance for picking up an item"""
        utters = [
            "You picked up the {i}.".format(i=item),
            "The {i} was added to your inventory.".format(i=item),
            "You took the {i}.".format(i=item),
        ]
        return random.choice(utters)
    
    ############################################################
    # Action utterances
    @classmethod
    def enter_room(cls, room: str, adventure=None) -> str:
        """Return the utterance for entering a room previously visited"""
        if not adventure:
            return "You entered {r}".format(r=room)
        else:
            return adventure.get_room(room).enter()

    
    @classmethod
    def cannot_move(cls, room: str, reason: str = None, possible_destinations: str = []) -> str:
        """Return the utterance for not allowing movement"""
        if possible_destinations:
            if reason == "locked":
                p = "You should figure out a way to get through or you could go to the {p}.".format(p=Text.properly_format_list(possible_destinations, delimiter=", the ", last_delimiter=" or the "))
            else:
                p = "You could go to the {p}.".format(p=Text.properly_format_list(possible_destinations, delimiter=", the ", last_delimiter=" or the "))
        else:
            p = ""
        if not reason:
            return "You cannot move to {room}. {p}".format(room=room, p=p)
        elif reason == "same":
            return "You cannot move to {room} because you're already there! {p}".format(
                room=room, p=p)
        elif reason == "locked":
            return "You cannot move to {room} because the way is locked! {p}".format(
                room=room, p=p)
        elif reason == "not connected":
            return "You cannot move to {room} because it's not connected to this room. {p}".format(
                room=room, p=p)
        elif reason == "no visibility":
            return "You cannot move to {room} because it's too dark for you to find the way!".format(
                room=room, p=p)
        elif reason == "no quest":
            return "You cannot move to {room} because you haven't spoken to Corvus or accepted the quest!".format(
                room=room, p=p)
        elif reason == "must kill":
            return "You cannot move to {room} because there are monsters in here you must deal with!".format(
                room=room)
        elif reason == "unknown destination":
            return "You cannot move to unknown room: {room}! {p}".format(
                room=room, p=p)
        else:
            return "You cannot move to {room}, although, I'm not sure why not... {p}".format(
                room=room, p=p)

    @classmethod
    def cannot_use(cls, equipment: str, reason: str = None) -> str:
        """Return the utterance for not allowing use of equipment"""
        if not reason:
            return "You cannot use {e}".format(e=equipment)
        elif reason == "unknown":
            return "You cannot use unknown equipment: {e}!".format(e=equipment)
        elif reason == "not equipped":
            return "You cannot use {e} because it's not equipped!".format(
                e=equipment)
        elif reason == "quantity":
            return "You cannot use {e} because you've run out!".format(
                e=equipment)
        elif reason == "unknown item":
            return "You cannot use unknown item: {e}!".format(
                e=equipment)
        elif reason == "not in inventory":
            return "You cannot use {e} because it's not in your inventory!".format(
                e=equipment)

    @classmethod
    def cannot_converse(cls, target: str, reason: str = None) -> str:
        """Return the utterance for not allowing converse of equipment"""
        if not reason:
            return "You cannot converse with {t}".format(t=target)
        elif reason == "unknown":
            return "You cannot converse with unknown entity: {t}!".format(t=target)
        elif reason == "monster":
            return "You try to converse with {t} but it's pointless as the monster can't understand.".format(
                t=target)
        elif reason == "different location":
            return "You cannot converse with {t} as it's not in the same location as you!".format(t=target)

    @classmethod
    def no_destination(cls, possible_destinations: list = []) -> str:
        """Return the utterance for no destination"""
        utters = [
            "Can you confirm your destination.",
            "Sorry, where do you want to go?",
            "I'm not sure where you want to go, can you repeat your destination.",
        ]
        
        if possible_destinations:
            p = "You could go to the {p}.".format(p=Text.properly_format_list(possible_destinations, delimiter=", the ", last_delimiter=" or the "))
        else:
            p = ""
        
        return "{u} {p}".format(u=random.choice(utters), p=p)

    @classmethod
    def no_target(cls, verb: str, possible_targets: str = "") -> str:
        """Return the utterance for no target"""
        utters = [
            "Can you confirm your target. {p}".format(p=possible_targets),
            "Who, or what, do you want to {v}? {p}".format(v=verb, p=possible_targets),
            "I'm not sure who or what you want to {v}. {p}".format(v=verb, p=possible_targets),
        ]
        return random.choice(utters)

    @classmethod
    def no_monster_targets(cls) -> str:
        """Return the utterance for no mosnter targets"""
        utters = [
            "There are no monsters in here for you to attack!",
            "You don't have any targets in here",
            "Nope, there are no monsters here"
        ]
        return random.choice(utters)
    
    @classmethod
    def no_equipment(cls, stop: bool = False) -> str:
        """Return the utterance for no equipment"""
        if stop:
            utters = [
                "Can you confirm the equipment you want to stop using",
                "Sorry, what do you want to stop using?",
                "I'm not sure what you want to stop using, can you repeat the equipment",
            ]
        else:
            utters = [
                "Can you confirm the equipment you want to use",
                "Sorry, what do you want to use?",
                "I'm not sure what you want to use, can you repeat the equipment",
            ]
        return random.choice(utters)

    @classmethod
    def no_weapon(cls, unequip: bool = False) -> str:
        """Return the utterance for no weapon"""
        if unequip:
            utters = [
                "Can you confirm the weapon you want to unequip",
                "Sorry, what do you want to unequip?",
                "I'm not sure what you want to unequip, can you repeat the weapon",
            ]
        else:
            utters = [
                "Can you confirm the weapon you want to equip",
                "Sorry, what do you want to equip?",
                "I'm not sure what you want to equip, can you repeat the weapon",
            ]
        return random.choice(utters)

    @classmethod
    def no_item(cls) -> str:
        """Return the utterance for no item"""
        utters = [
            "Can you confirm the item you want to pick up",
            "Sorry, what do you want to pick up?",
            "I'm not sure what you want to pick up, can you repeat the item",
        ]
        return random.choice(utters)
    
    @classmethod
    def cannot_pick_up(cls, item: str, reason: str = None) -> str:
        """Return the utterance for not allowing picking up item"""
        if not reason:
            return "You cannot pick up {i}".format(i=item)
        elif reason == "not in room":
            return "You cannot pick up {i} because it's not in this room!".format(i=item)
        elif reason == "no visibility":
            return "You cannot pick up {i} because it's too dark to see it!".format(i=item)
        elif reason == "unknown entity":
            return "You cannot pick up {i}".format(i=item)
    
    @classmethod
    def cannot_equip(cls, weapon: str, reason: str = None) -> str:
        """Return the utterance for not allowing equipping of weapon"""
        if not reason:
            return "You cannot equip {w}".format(w=weapon)
        elif reason == "unknown":
            return "You cannot equip unknown equipment: {w}!".format(w=weapon)
        elif reason == "not owned":
            return "You cannot equip {w} because it's not in your inventory!".format(
                w=weapon)
        elif reason == "no free slots":
            return "You cannot equip {w} because you don't have any free slots! Unequip something first.".format(
                w=weapon)
        elif reason == "already equipped":
            return "You cannot equip {w} because it's already equipped!".format(
                w=weapon)

    @classmethod
    def cannot_unequip(cls, weapon: str, reason: str = None) -> str:
        """Return the utterance for not allowing unequipping of weapon"""
        if not reason:
            return "You cannot unequip {w}".format(w=weapon)
        elif reason == "unknown":
            return "You cannot unequip unknown equipment: {w}!".format(w=weapon)
        elif reason == "not owned":
            return "You cannot unequip {w} because it's not in your inventory!".format(
                w=weapon)
        elif reason == "not equipped":
            return "You cannot unequip {w} because it's not equipped!".format(
                w=weapon)
        elif reason == "nothing equipped":
            return "You cannot unequip because nothing is equipped!"

    @classmethod
    def equip_weapon(cls, weapon: str) -> str:
        """Return the utterance for equipping a weapon"""
        utters = [
            "You equipped {w}".format(w=weapon)
        ]
        return random.choice(utters)

    @classmethod
    def unequip_weapon(cls, weapon: str) -> str:
        """Return the utterance for unequipping a weapon"""
        if not weapon:
            return "You unequipped all weapons."
        utters = [
            "You unequipped {w}".format(w=weapon)
        ]
        return random.choice(utters)

    @classmethod
    def light_torch(cls) -> str:
        """Return the utterance for lighting a torch"""
        utters = [
            "You light a torch and the space around you is now lighter.",
            "The space around you illuminates in the glow of your lit torch.",
            "Light now cascades from the point of your torch around you."
        ]
        return random.choice(utters)

    @classmethod
    def extinguish_torch(cls) -> str:
        """Return the utterance for extinguishing a torch"""
        utters = [
            "You extinguish your torch and the space around you is now darker.",
            "The space around you returns to its normal light level.",
            "Light ceases to cascade from your torch."
        ]
        return random.choice(utters)

    ############################################################
    # Combat utterances
    @classmethod
    def transition_to_combat(cls) -> str:
        """Return the utterance for transitioning to combat"""
        utters = [
            "Okay let's fight, roll for initiative!", "You're now starting combat, roll for initiative!",
            "Let's begin the combat round, roll for initiative!", "Moving into combat, roll for initiative!"
        ]
        return random.choice(utters)

    @classmethod
    def entity_turn(cls, entity: str) -> str:
        """Return the utterance for telling the player whose turn it is"""
        entity = "your" if entity == "player" else "{e}'s".format(e=entity)
        utters = [
            "Okay, it's {e} turn...".format(e=entity)
        ]
        return random.choice(utters)
    
    @classmethod
    def declare_attack(cls) -> str:
        """Return the utterance for getting player to declare an attack"""
        utters = [
            "Your turn, who do you want to attack?"
        ]
        return random.choice(utters)
    
    @classmethod
    def perform_attack_roll(cls) -> str:
        """Return the utterance for getting player to perform attack roll"""
        utters = [
            "Make your attack roll"
        ]
        return random.choice(utters)

    @classmethod
    def perform_damage_roll(cls) -> str:
        """Return the utterance for getting player to perform damage roll"""
        utters = [
            "Make your damage roll"
        ]
        return random.choice(utters)
    
    @classmethod
    def attack(cls, attacker: str, target: str, *args) -> str:
        """Return the utterance for attacking"""
        # TODO different utterances for different weapons?
        attacker = "You" if attacker == "player" else attacker
        utters = [
            "{a} attacked {t}!".format(a=attacker, t=target),
            "{a} launched an assault on {t}".format(a=attacker, t=target),
            "{a} struck at {t}".format(a=attacker, t=target),
        ]
        return random.choice(utters)

    @classmethod
    def cannot_attack(cls, attacker: str, target: str, name: str, reason: str = None, possible_targets: list = []) -> str:
        """Return the utterance for not allowing attack"""
        if attacker == "player" or attacker == name:
            attacker = "You"
        
        if possible_targets:
            p = "You could target {p}".format(p=possible_targets[0])
            for poss in possible_targets[1:]:
                if possible_targets[-1] == poss:
                    p += " or the {p}".format(p=poss)
                else:
                    p += ", the {p}".format(p=poss)
                    
        if not reason:
            return "{a} cannot attack {t}".format(a=attacker, t=target)
        elif reason == "unknown target":
            return "{a} cannot attack unknown target: {t}!".format(a=attacker, t=target)
        elif reason == "different location":
            return "{a} cannot attack {t} as it's not in the same location as you!".format(a=attacker, t=target)
        elif reason == "no visibility":
            return "{a} cannot attack {t} because it's too dark to see them!".format(
                a=attacker, t=target) 
        elif reason == "dead target":
            return "{a} cannot attack {t} because they're already dead!".format(
                a=attacker, t=target) 
        elif reason == "no weapon":
            return "{a} cannot attack {t} because you have no equipped weapons! Try equipping a weapon first.".format(
                a=attacker, t=target) 
    
    @classmethod
    def attack_of_opportunity(cls,
                              attacker: str = None,
                              target: str = None) -> str:
        """Return the utterance for an attack of opportunity"""
        if target and attacker:
            utters = [
                "{a} took an attack of opportunity against {t}!".format(
                    a=attacker, t=target),
                "{t} opened themselves up to an an attack of opportunity from {a}!"
                .format(a=attacker, t=target)
            ]
            return random.choice(utters)
        elif attacker:
            utters = [
                "{a} took an attack of opportunity against you!".format(
                    a=attacker),
                "You opened yourself up to an an attack of opportunity from {a}!"
                .format(a=attacker)
            ]
            return random.choice(utters)
        elif target:
            utters = [
                "You took an attack of opportunity against {t}!".format(
                    t=target),
                "{t} opened themselves up to an an attack of opportunity from you!"
                .format(t=target)
            ]
            return random.choice(utters)
    
    @classmethod
    def won_fight(cls) -> str:
        """Method to return the utterance for winning a fight"""
        utters = [
            "You won the battle, congratulations!",
            "You put up a good fight and it paid off",
            "Awesome, they won't be bothering you again!"
        ]
        return random.choice(utters)

    ############################################################
    # Roleplay utterances
    @classmethod
    def roleplay(cls, name: str, target: str) -> str:
        """Return the utterance for getting roleplay prompt"""
        utters = [
            "{n}, what do you say to {t}?".format(n=name, t=target)
        ]
        return random.choice(utters)

    @classmethod
    def drink_ale(cls, ales: int) -> str:
        """Return the utterance for drinking an ale"""
        utters = [
            "The barkeep pours you a frothy golden ale, which you finish in a few big gulps.",
            "You are served a beautiful dark ale, which you savour over the course of half an hour. Delightful!",
            "The barkeep presents you with a cloudy pale ale. You take an experimental sip and you're in ale heaven! You down the whole glass."
        ]
        return utters[ales]

    ############################################################
    # Query utterances
    @classmethod
    def explain_armor_class(cls) -> str:
        """Return the utterance for explaining a armos class"""
        return "The minimum roll for successful damage. It is calculated as [x] because of [x, y, z]."

    @classmethod
    def explain_critical(cls) -> str:
        """Return the utterance for explaining a critical hit"""
        return "Critical means the damage dice are doubled. Roll for damage, double that, and add your modifier after that."

    ############################################################
    # Exploration and investigation utterances
    @classmethod
    def cannot_investigate(cls, target: str, reason: str = None) -> str:
        """Return the utterance for not allowing investigate of target"""
        if not reason:
            return "You cannot investigate {t}".format(t=target)
        elif reason == "unknown entity":
            return "You cannot investigate unknown target: {t}!".format(t=target)
        elif reason == "different location":
            return "You cannot investigate target {t}, you're not in the same location!".format(t=target)
        elif reason == "no visibility":
            return "You cannot investigate because it's too dark to see anything!".format()

    ############################################################
    # Dealing with doors utterances
    @classmethod
    def no_door_targets(cls, verb: str) -> str:
        """Return the utterance for no door targets"""
        utters = [
            "There are no doors here you need to {v}!".format(v=verb),
            "There aren't any suitable door targets here.",
            "Nope, there are no doors you need to {v} here.".format(v=verb)
        ]
        return random.choice(utters)
    
    @classmethod
    def no_door_target(cls, verb: str, possible_targets: str = "") -> str:
        """Return the utterance for no door target"""
        utters = [
            "Can you confirm your door target. {p}".format(p=possible_targets),
            "What door do you want to {v}? {p}".format(v=verb, p=possible_targets),
            "I'm not sure what door you want to {v}. {p}".format(v=verb, p=possible_targets),
        ]
        return random.choice(utters)
    
    @classmethod
    def broke_down_door(cls, target: str) -> str:
        """Return the utterance for no door target"""
        utters = [
            "You destroyed the door to the {t}.".format(t=target),
            "You broke down the {t} door.".format(t=target),
            "The door to the {t} is now a mess of splinters on the floor.".format(t=target),
        ]
        return random.choice(utters)

    @classmethod
    def deal_door_damage(cls, damage: int, hp: int) -> str:
        """Return the utterance for dealing damage to door"""
        if damage <= 0.25*hp:
            utters = [
                "The hit barely registers, you're going to be here a while.",
                "You've dealt some damage... not that much though.",
                "You've damaged the door a little. There might be a better way to deal with this."
            ]
        elif damage <= 0.5*hp:
            utters = [
                "That was a decent hit.",
                "You did a good amount of damage to the door.",
                "The door won't withstand a lot of this."
            ]
        else:
            utters = [
                "That's a lot of damage!",
                "The door has no chance when you're dealing damge like this!",
                "Boom! That's how you do it!"
            ]
        return random.choice(utters)
    
    @classmethod
    def cannot_attack_door(cls, attacker: str, target: str, name: str, reason: str = None, possible_targets: list = []) -> str:
        """Return the utterance for not allowing door attack"""
        if attacker == "player" or attacker == name:
            attacker = "You"
        
        if possible_targets:
            p = "You could target the door to the {p}".format(p=possible_targets[0])
            for poss in possible_targets[1:]:
                if possible_targets[-1] == poss:
                    p += " or the {p}".format(p=poss)
                else:
                    p += ", the {p}".format(p=poss)
                    
        if not reason:
            return "{a} cannot attack {t}".format(a=attacker, t=target)
        elif reason == "unknown target":
            return "{a} cannot attack unknown target: {t}!".format(a=attacker, t=target)
        elif reason == "different location":
            return "{a} cannot attack {t} as it's not in the same location as you!".format(a=attacker, t=target)
        elif reason == "no visibility":
            return "{a} cannot attack {t} because it's too dark to see it!".format(
                a=attacker, t=target) 
        elif reason == "destroyed door":
            return "{a} cannot attack {t} because it's already destroyed!".format(
                a=attacker, t=target) 
        elif reason == "travel allowed":
            return "{a} cannot attack {t} because it's already open!".format(
                a=attacker, t=target) 
        elif reason == "no weapon":
            return "{a} cannot attack {t} because you have no equipped weapons! Try equipping a weapon first.".format(
                a=attacker, t=target) 
    
    @classmethod
    def not_force_target(cls, target: str) -> str:
        """Return the utterance for not a force target"""
        utters = [
            "{t} is not a target that can be forced.".format(t=target),
            "You cannot force a this target.".format(t=target),
            "Yeh, I'm not allowing you to force {t}.".format(t=target),
        ]
        return random.choice(utters)
    
    ############################################################
    # Ability and skill check utterances
    @classmethod
    def ability_check(cls, ability: str, dm_request: bool = False) -> str:
        """Return the utterance for performing ability check"""
        n = "an" if ability == "Intelligence" else "a"
        if dm_request:
            utters = [
                "Actually, go ahead and do {n} {a} check.".format(a=ability, n=n),
                "I'd like you to do {n} {a} roll.".format(a=ability, n=n),
                "You know what, go ahead and do {n} {a} roll.".format(a=ability, n=n),
            ]
        else:
            utters = [
                "Okay, go ahead and do {n} {a} check.".format(a=ability, n=n),
                "Okay, do {n} {a} roll.".format(a=ability, n=n),
                "Sure, go ahead and do {n} {a} roll.".format(a=ability, n=n),
            ]
        return random.choice(utters)
    
    @classmethod
    def cannot_ability_check(cls, ability: str, target: str, reason: str = None) -> str:
        """Return the utterance for not allowing ability check"""
        n = "an" if ability == "Intelligence" else "a"
        if not reason:
            return "You cannot perform {a} check.".format(a=ability)
        elif reason == "different location":
            return "You cannot perform {a} check on {t} because it's not in this room!".format(a=ability, t=target)
        elif reason == "no visibility":
            return "You cannot perform {a} check because it's too dark to see anything!".format(a=ability)
        elif reason == "unknown entity":
            return "You cannot perform {a} check on unknown target {t}".format(a=ability, t=target)
        elif reason == "not required":
            return "You don't need to perform {n} {a} check in this situation.".format(a=ability, n=n)
        elif reason == "unknown room":
            return "You cannot perform {a} check on unknown target {t}".format(a=ability, t=target)

    @classmethod
    def skill_check(cls, skill: str, dm_request: bool = False) -> str:
        """Return the utterance for performing skill check"""
        n = "an" if skill in ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Insight", "Intimidation", "Investigation"] else "a"
        if dm_request:
            utters = [
                "Actually, go ahead and do {n} {s} check.".format(s=skill, n=n),
                "I'd like you to do {n} {s} roll.".format(s=skill, n=n),
                "You know what, go ahead and do {n} {s} roll.".format(s=skill, n=n),
            ]
        else:
            utters = [
                "Okay, go ahead and do {n} {s} check.".format(s=skill, n=n),
                "Okay, do {n} {s} roll.".format(s=skill, n=n),
                "Sure, go ahead and do {n} {s} roll.".format(s=skill, n=n),
            ]
        return random.choice(utters)
    
    @classmethod
    def cannot_skill_check(cls, skill: str, target: str, reason: str = None) -> str:
        """Return the utterance for not allowing skill check"""
        n = "an" if skill in ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Insight", "Intimidation", "Investigation"] else "a"
        if not reason:
            return "You cannot perform {s} check.".format(s=skill)
        elif reason == "different location":
            return "You cannot perform {s} check on {t} because it's not in this room!".format(s=skill, t=target)
        elif reason == "no visibility":
            return "You cannot perform {s} check because it's too dark to see anything!".format(s=skill)
        elif reason == "unknown entity":
            return "You cannot perform {s} check on unknown target {t}".format(s=skill, t=target)
        elif reason == "not required":
            return "You don't need to perform {n} {s} check in this situation.".format(s=skill, n=n)
        elif reason == "unknown room":
            return "You cannot perform {s} check on unknown target {t}".format(s=skill, t=target)

    @classmethod
    def succeed_check(cls) -> str:
        """Return the utterance for succeeding on an ability check"""
        utters = [
            "You did it!",
            "That works.",
            "That succeeds.",
        ]
        return random.choice(utters)
    
    @classmethod
    def fail_check(cls, allow_repeat: bool = True) -> str:
        """Return the utterance for failing on an ability check"""
        if allow_repeat:
            r = "You could try again or do something different."
        else:
            r = "You're going to have to try something else."
        utters = [
            "You didn't do it. {r}".format(r=r),
            "That didn't work. {r}".format(r=r),
            "That fails. {r}".format(r=r)
        ]
        return random.choice(utters)
    
    @classmethod
    def no_reason_roll(cls) -> str:
        """Return the utterance for rolling for no reason"""
        utters = [
            "Rolling dice is fun!",
            "I don't know what you're rolling for, but it's fun anyway!",
            "Okay, you rolled your dice... now what??",
        ]
        return random.choice(utters)
    
    ############################################################
    # Gameover utterances
    @classmethod
    def attack_npc_end_game(cls, name: str) -> str:
        """Return the utterance for ending the game by attacking npc"""
        utters = [
            "You attacked and fatally wounded {n}. He was a much loved member of the community and retribution was swift. You were captured within the day and currently languish in a miserable cell in the Greyforge city jail, awaiting trial."
            .format(n=name),
            "Your unprovoked attack took your good friend {n} completely unawares. As the light left his eyes, he managed to utter a quiet \"why?\" with his dying breath. Why indeed? You were captured within the day and currently languish in a miserable cell in the Greyforge city jail, awaiting trial."
            .format(n=name),
            "Not known for reasonable, measured behaviour you irrationally lashed out at {n}. The elderly dwarf had no time to defend himself, but let out a shout as he succumbed to his injury. Overheard by the city guard, you were promptly captured and currently languish in a miserable cell in the Greyforge city jail, awaiting trial."
            .format(n=name),
        ]
        return random.choice(utters)
    
    @classmethod
    def hp_end_game(cls, entity: str, death_text: str = "") -> str:
        """Return the utterance for ending the game by running out of hp"""
        utters = [
            "You were attacked and fatally wounded by {e}. {d}".format(e=entity, d=death_text),
            "{e} killed you! {d}".format(e=entity, d=death_text),
            "Nooo, you tried your hardest but it wasn't to be. {d}".format(e=entity, d=death_text),
        ]
        return random.choice(utters)
    
    @classmethod
    def drunk_end_game(cls) -> str:
        """Return the utterance for ending the game by drinking too much"""
        utters = [
            "Onto your fourth drink and you completely forgot the reason you came here. You while away the day drinking good ale with fine company. It was a good day!",
        ]
        return random.choice(utters)