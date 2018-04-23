from src.characters.datatypes import Player
from src.objects.armour import ringmail, make_armour
from src.objects.food import foods, make_food
from src.objects.weapons import arrow, mace, make_weapon, shortbow


def make_player():
    sb = make_weapon(shortbow)
    sb.attack_mod = 1
    sb.dexterity_mod = 1
    sb.name = sb.realname
    ar = make_weapon(arrow)
    ar.attack_mod = 0
    ar.dexterity_mod = 0
    ar.name = ar.realname
    mc = make_weapon(mace)
    mc.attack_mod = 2
    mc.dexterity_mod = 2
    mc.name = mc.realname
    player = Player(weapon=mc,
                    armour=make_armour(ringmail),
                    items=[sb,
                           ar,
                           make_food(foods[0]),
                           ]
                    )
    player.inventory['d'].count = 30
    return player
