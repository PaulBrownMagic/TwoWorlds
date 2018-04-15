from types import FunctionType

from tcod import color

from src.maps.datatypes import Location


class Object:
    name: str
    location: Location
    char: str
    colour: color.Color
    blocks: bool

    def __init__(self, name, location, char, colour):
        self.name = name
        self.location = location
        self.char = char
        self.colour = colour
        self.blocks = False


class MovingObject(Object):
    state: str
    attack: int
    defence: int
    hp: int

    def __init__(self, name, location, char, colour,
                 state, attack, defence, hp):
        super().__init__(name, location, char, colour)
        self.state = state
        self.attack = attack
        self.defence = defence
        self.hp = hp
        self.blocks = True


class Item(Object):
    weight: int = 1


class FunctioningItem(Item):
    function: FunctionType

    def __init__(self, name, location, char, colour, function):
        super().__init__(name, location, char, colour)
        self.function = function


class Armour(Item):
    defence: int

    def __init__(self, name, location, char, colour, defence):
        super().__init__(name, location, char, colour)
        self.defence = defence


class Weapon(Item):
    attack: int
    precision: int

    def __init__(self, name, location, char, colour, attack, precision):
        super().__init__(name, location, char, colour)
        self.attack = attack
        self.precision = precision


class Projectile(Weapon, FunctioningItem):

    def __init__(self, name, location, char, colour, attack, precision):
        super().__init__(name, location, char, colour, attack, precision)
        self.function = None  # Must write


class Monster(MovingObject):
    targeting_condition: FunctionType
    target: Location


class Player(MovingObject):
    max_attack: int = 16
    xp_level: int = 1
    xp: int = 0
    carrying_weight_limit: int = 14
    inventory: list = []
    wearing: Armour = None
    weilding: Weapon = None
    # rings: [Rings] = []


class MagicMonster(Monster):
    pass


class MagicItem(FunctioningItem):
    pass


class MagicWand(Projectile):
    pass
