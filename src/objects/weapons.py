from random import choices

from src.objects.datatypes import Weapon, Projectile

from tcod import color as colour

W_COLOUR = colour.white

mace = dict(name="Mace", damage="2d4", p=4)
longsword = dict(name="Longsword", damage="3d4", p=2)
shortbow = dict(name="Short Bow", damage="1d1", p=3)
twosword = dict(name="Two Handed Sword", damage="4d4", p=1)


arrow = dict(name="Arrow", damage="1d3", thrown="2d3", p=3)
dagger = dict(name="Dagger", damage="1d6", thrown="1d4", p=4)
dart = dict(name="Dart", damage="1d2", thrown="1d3", p=3)
shuriken = dict(name="Shuriken", damage="1d2", thrown="2d4", p=2)
spear = dict(name="Spear", damage="2d3", thrown="1d6", p=1)

weapons = [mace, longsword, shortbow, twosword]
projectiles = [arrow, dagger, dart, shuriken, spear]
all_weapons = weapons + projectiles

weights = [1, 2, 10, 3, 2]
mods = [-2, -1, 0, 1, 2]


def make_weapon(w):
    if w in weapons:
        return Weapon(name=w['name'],
                      char=")",  # ] for armour
                      colour=W_COLOUR,
                      attack=w['damage'],
                      attack_mod=choices(mods, weights)[0],
                      dexterity_mod=choices(mods, weights)[0],
                      )
    elif w in projectiles:
        return Projectile(name=w['name'],
                          char=")",
                          colour=W_COLOUR,
                          attack=w['damage'],
                          thrown=w['thrown'],
                          attack_mod=choices(mods, weights)[0],
                          dexterity_mod=choices(mods, weights)[0],
                          )


def get_x_weapons(num):
    weights = [w['p'] for w in all_weapons]
    return list(map(make_weapon, choices(all_weapons, weights, k=num)))
