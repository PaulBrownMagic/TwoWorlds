from random import randint, choice

from tcod import color as colour

from src.objects.datatypes import Monster
from src.objects.combat import dice_roll
from src.objects.magicmonsters import SL, SN, A, STATES, magic_monsters
from src.maps import distance_to

M_COLOUR = colour.white


def in_room_target(monster, level):
    if distance_to(monster.location, level.player.location) < 14:
        monster.state = "TARGETING"


# flags: A: armour drain, M: mean, F: flying, H: hidden, R: regen hp,
# V: drain hp, X: drain xp, S: stationairy, L: lure player


nd = dict(name="Dodo", levels=(1, 3), carry=0, flags="",
          xp=1, ac=9, hp="1d8", dmg="1d2", state=SL)
nq = dict(name="Quokka", levels=(1, 4), carry=0, flags="",
          xp=2, ac=8, hp="1d8", dmg="1d2", state=SN)
ne = dict(name="Emu", levels=(1, 5), carry=0, flags="M",
          xp=4, ac=7, hp="1d8", dmg="1d4", state=A)
nc = dict(name="Cockroach", levels=(3, 8), carry=0, flags="R",
          xp=8, ac=6, hp="3d8", dmg="1d2", state=SN)
nf = dict(name="Falcon", levels=(4, 7), carry=0, flags="MF",
          xp=7, ac=7, hp="2d8", dmg="1d4", state=A)
ns = dict(name="Scorpian", levels=(5, 9), carry=0, flags="M",
          xp=10, ac=6, hp="2d8", dmg="1d6", state=SL)
nl = dict(name="Llama", levels=(6, 10), carry=0, flags="",
          xp=9, ac=7, hp="2d8", dmg="1d4", state=A)
ni = dict(name="Iguana", levels=(7, 12), carry=0, flags="",
          xp=10, ac=7, hp="3d8", dmg="1d5", state=A)
nb = dict(name="Bandit", levels=(8, 14), carry=25, flags="M",
          xp=28, ac=5, hp="4d8", dmg="1d8", state=A)
nh = dict(name="Hobo", levels=(9, 12), carry=10, flags="",
          xp=12, ac=8, hp="5d8", dmg="1d4", state=SL)
nv = dict(name="Viper", levels=(10, 15), carry=0, flags="M",
          xp=36, ac=7, hp="3d8", dmg="1d6", state=SN)
no = dict(name="Orangutan", levels=(11, 16), carry=0, flags="",
          xp=18, ac=8, hp="4d8", dmg="1d5", state=A)
nj = dict(name="Jaguar", levels=(13, 19), carry=0, flags="",
          xp=25, ac=6, hp="4d8", dmg="1d6", state=SN)
nm = dict(name="Mercenary", levels=(14, 18), carry=0, flags="M",
          xp=55, ac=6, hp="6d8", dmg="1d8", state=A)
nt = dict(name="Tarantula", levels=(15, 19), carry=0, flags="",
          xp=50, ac=8, hp="5d8", dmg="1d8", state=SN)
na = dict(name="Alligator", levels=(16, 22), carry=0, flags="",
          xp=80, ac=7, hp="6d8", dmg="2d6", state=SL)
ng = dict(name="Gorilla", levels=(17, 999), carry=0, flags="M",
          xp=190, ac=6, hp="6d8", dmg="2d5", state=SN)
np = dict(name="Pirate", levels=(20, 24), carry=50, flags="",
          xp=120, ac=5, hp="7d8", dmg="2d6", state=A)
nw = dict(name="Warrior", levels=(19, 25), carry=0, flags="",
          xp=350, ac=4, hp="9d8", dmg="3d4", state=A)
nr = dict(name="Rhinoceros", levels=(20, 999), carry=0, flags="",
          xp=2000, ac=4, hp="11d8", dmg="2d12", state=SN)
nn = dict(name="Ninja", levels=(23, 999), carry=50, flags="MHR",
          xp=3000, ac=7, hp="10d8", dmg="2d8", state=SN)
nk = dict(name="Knight", levels=(24, 999), carry=100, flags="M",
          xp=5000, ac=1, hp="15d8", dmg="3d10", state=A)


normal_monsters = [na, nb, nc, nd, ne, nf, ng, nh, ni, nj, nk, nl, nm, nn, no,
                   np, nq, nr, ns, nt, nv, nw]

monsters = dict(NORMAL=normal_monsters,
                MAGIC=magic_monsters)


def make_monster(m):
    return Monster(name=m['name'],
                   char=m['name'][0],
                   colour=M_COLOUR,
                   state=m['state'] if randint(1, 10) < 9 else choice(STATES),
                   attack=m['dmg'],
                   armour=m['ac'],
                   hp=dice_roll(m['hp']),
                   xp=m['xp'],
                   flags=m['flags'],
                   carry=m['carry'],
                   )


def monsters_for(level):
    i = level.number
    return [m for m in monsters[level.world]
            if min(m['levels']) <= i and max(m['levels']) >= i]


def get_x_monsters_for(num, level):
    appropriate_monsters = monsters_for(level)
    return [make_monster(choice(appropriate_monsters)) for _ in range(num)]
