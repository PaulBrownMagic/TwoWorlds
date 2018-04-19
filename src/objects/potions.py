from itertools import chain
from random import randint, choices

from tcod import color as colour

from src.gui import message
from src.objects.datatypes import Potion, PotionName

P_COLOUR = colour.white


def confuse(level):
    """Confuses Player"""
    message("Rogue is confused")
    level.player.state = "CONFUSED1234567"


def hallucinate(level):
    pass


def poison(level):
    message("Rogue feels weaker")
    level.player.strength -= randint(1, 3)


def gain_strength(level):
    message("Rogue feels stronger")
    level.player.strength += 1
    if level.player.strength > level.player.max_strength:
        level.player.max_strength = level.player.strength


def restore_stength(level):
    message("That tastes good. Rogue feels warm all over")
    level.player.strength = level.player.max_strength


def see_hidden(level):
    pass


def blindness(level):
    level.player.state = "BLIND_300"
    for tile in chain(*level.map_grid.tiles):
        tile.explored = False
    message("A veil of darkness falls around you")


def heal(level):
    """Heal Player"""
    level.player.hp += randint(1, 1 + level.player.xp_level)
    if level.player.hp >= level.player.max_hp:
        level.player.max_hp += 1
        level.player.hp = level.player.max_hp
    level.player.state = "ACTIVE"
    message("Rogue feels better")


def extra_healing(level):
    """Extra healing for Player"""
    hp = level.player.hp
    max_hp = level.player.max_hp
    level.player.hp += sum([randint(1, 8) for _ in range(level.player.xp_level)])
    if hp >= max_hp:
        level.player.max_hp += randint(1, 2)
        level.player.hp = level.player.max_hp
    level.player.state = "ACTIVE"
    message("Rogue feels *much* better")


def monster_detect(level):
    """View all monsters"""
    for monster in level.monsters:
        monster.found = True
    message("Rogue's instincts are heightened")


def item_detect(level):
    """View all items"""
    for item in level.items:
        item.found = True
    message("Rogue's senses are heightened")


def xp_up(level):
    """Level up player"""
    p = level.player
    p.xp = p.xp_to_level_up + 1
    p.xp_level += 1
    hp_up = randint(3, 15)
    p.hp += hp_up
    p.max_hp += hp_up
    message("Rogue gained experience")


Name = PotionName

potions = [dict(name=Name("Confusion"), p=7, f=confuse),
           # dict(name=Name('Hallucination'), p=8, f=hallucinate),
           dict(name=Name('Poison'), p=8, f=poison),
           dict(name=Name("Gain Strength"), p=13, f=gain_strength),
           dict(name=Name("See Hidden"), p=3, f=see_hidden),
           dict(name=Name("Healing"), p=13, f=heal),
           dict(name=Name("Monster Detection"), p=6, f=monster_detect),
           dict(name=Name("Item Detection"), p=6, f=item_detect),
           dict(name=Name("Raise Level"), p=2, f=xp_up),
           dict(name=Name("Extra Healing"), p=5, f=extra_healing),
           dict(name=Name("Restore Strength"), p=13, f=restore_stength),
           dict(name=Name("Blindness"), p=5, f=blindness),
           ]


def make_potion(p):
    return Potion(name=p['name'],
                  char="!",
                  colour=P_COLOUR,
                  function=p['f']
                  )


def get_x_potions(num):
    weights = [p['p'] for p in potions]
    return list(map(make_potion, choices(potions, weights, k=num)))
