from src.objects.datatypes import Weapon, Projectile

from tcod import color as colour

W_COLOUR = colour.white

mace = dict(name="mace", damage="2d4")
longsword = dict(name="longsword", damage="3d4")
shortbow = dict(name="short bow", damage="1d1")
twosword = dict(name="two handed sword", damage="4d4")


arrow = dict(name="arrow", damage="1d3", thrown="2d3")
dagger = dict(name="dagger", damage="1d6", thrown="1d4")
dart = dict(name="dart", damage="1d2", thrown="1d3")
shuriken = dict(name="shuriken", damage="1d2", thrown="2d4")
spear = dict(name="spear", damage="2d3", thrown="1d6")

weapons = [mace, longsword, shortbow, twosword]
projectiles = [arrow, dagger, dart, shuriken, spear]
all_weapons = weapons + projectiles


def make_weapon(w):
    if w in weapons:
        return Weapon(name=w['name'],
                      char=")",  # ] for armour
                      colour=W_COLOUR,
                      attack=w['damage']
                      )
    elif w in projectiles:
        return Projectile(name=w['name'],
                          char=")",
                          colour=W_COLOUR,
                          attack=w['damage'],
                          thrown=w['thrown']
                          )

