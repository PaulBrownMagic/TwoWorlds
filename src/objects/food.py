from random import choices, choice

from tcod import color as colour

from src.config import HUNGRY
from src.gui import message
from src.objects.datatypes import Food, Fruit


F_COLOUR = colour.darker_grey


def eat(level):
    level.player.hunger = 0


def snack(level):
    level.player.hunger -= HUNGRY
    if level.player.hunger < 0:
        level.player.hunger = 0


tastes = ["yummy", "yucky", "disgusting", "amazing",
          "like old boots", "like manna from heaven",
          "satisfactory", "fine"]

foods = [dict(name="food", p=7, f=eat),
         dict(name="fruit", p=3, f=snack)]


def make_food(f):
    kind = Food if f['name'] == "food" else Fruit
    return kind(name=f['name'],
                char=":",
                colour=F_COLOUR,
                function=f['f'],
                taste=choice(tastes)
                )


def get_x_foods(num):
    weights = [f['p'] for f in foods]
    return list(map(make_food, choices(foods, weights, k=num)))
