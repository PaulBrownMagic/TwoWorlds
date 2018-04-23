from tcod import color as colour

from src.objects.datatypes import Object, Armour, Weapon, Item, Food


class MovingObject(Object):
    state: str
    xp: int
    hp: int
    max_hp: int

    def __init__(self, name, char, colour,
                 state, hp, xp):
        super().__init__(name, char, colour)
        self.state = state
        self.hp = hp
        self.max_hp = hp
        self.blocks = True
        self.xp = xp


class Monster(MovingObject):
    attack: str
    armour: int
    flags: str

    def __init__(self, name, char, colour,
                 state, attack, armour, hp, xp, flags, carry):
        super().__init__(name, char, colour, state, hp, xp)
        self.attack = attack
        self.armour = armour
        self.flags = flags
        self.carry = carry


class Player(MovingObject):
    max_strength: int
    xp_level: int = 1
    xp: int = 0
    inventory: dict = {l: None for l in "abcdefghijklmnopqrstuvwxyz"}
    wearing: Armour = None
    wielding: Weapon = None
    has_amulet_of_yendor: bool = False
    inventory_limit = 26
    hunger: int = 0
    # rings: [Rings] = []

    def __init__(self, armour, weapon, items):
        super().__init__("Rogue", "@", colour.white, "ACTIVE", 12, 0)
        self.strength = 16
        self.max_strength = self.strength
        self.wearing = armour
        self.wielding = weapon
        self.inventory['a'] = InventoryItem(armour)
        self.inventory['b'] = InventoryItem(weapon)
        for l, i in zip("cdefghijklmnopqrstuvwxyz", items):
            if type(i) == Food:
                self.inventory[l] = InventoryItem(i, count=2, max_count=50)
            else:
                self.inventory[l] = InventoryItem(i)

    @property
    def xp_to_level_up(self):
        return 10*2**self.xp_level

    @property
    def attack(self):
        return self.wielding.attack if self.wielding is not None else "1d2"

    @property
    def armour(self):
        return self.wearing.defence if self.wearing is not None else 11


class InventoryItem:
    count: int
    item: Item
    full: bool

    def __init__(self, item, count=1, max_count=1):
        self.item = item
        self.count = count
        self.max_count = max_count

    def __str__(self):
        return self.item

    @property
    def full(self):
        return self.count == self.max_count

    @property
    def weight(self):
        return self.count * self.item.weight
