from tcod import color as colour

from src.objects.datatypes import Armour

A_COLOUR = colour.white

leather = dict(name="leather armour", ac=8)
ringmail = dict(name="ring mail", ac=7)
st_leather = dict(name="studded leather armour", ac=7)
scalemail = dict(name="scale mail", ac=6)
chainmail = dict(name="chain mail", ac=5)
splintmail = dict(name="splint mail", ac=4)
bandedmail = dict(name="banded mail", ac=4)
platemail = dict(name="plate mail", ac=3)

armours = [leather, ringmail, st_leather, scalemail, chainmail,
           splintmail, bandedmail, platemail]


def make_armour(a):
    return Armour(name=a['name'],
                  char="]",
                  colour=A_COLOUR,
                  defence=a['ac']
                  )
