from random import choices

from tcod import color as colour

from src.objects.datatypes import Armour

A_COLOUR = colour.white

leather = dict(name="leather armour", ac=8, p=5)
ringmail = dict(name="ring mail", ac=7, p=5)
st_leather = dict(name="studded leather armour", ac=7, p=1)
scalemail = dict(name="scale mail", ac=6, p=4)
chainmail = dict(name="chain mail", ac=5, p=3)
splintmail = dict(name="splint mail", ac=4, p=2)
bandedmail = dict(name="banded mail", ac=4, p=2)
platemail = dict(name="plate mail", ac=3, p=1)

armours = [leather, ringmail, st_leather, scalemail, chainmail,
           splintmail, bandedmail, platemail]


def make_armour(a):
    return Armour(name=a['name'],
                  char="]",
                  colour=A_COLOUR,
                  defence=a['ac']
                  )


def get_x_armours(num):
    weights = [a['p'] for a in armours]
    return list(map(make_armour, choices(armours, weights, k=num)))
