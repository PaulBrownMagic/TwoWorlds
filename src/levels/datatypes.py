from src.maps.datatypes import Map
from src.objects.datatypes import (Item,
                                   Stairs,
                                   MagicItem,
                                   Player,
                                   Monster,
                                   MagicMonster)


class Level:
    map_grid: Map
    player: Player
    stairs: Stairs
    items: [Item]
    monsters: [Monster]
    number: int
    complete: bool = False
    world: str = "NORMAL"

    def __init__(self, number, player, stairs, items, monsters):
        self.number = number
        self.player = player
        self.stairs = stairs
        self.map_grid = Map()
        self.items = items
        self.monsters = monsters

    @property
    def all_objects(self):
        return self.items + self.monsters


class MagicLevel(Level):
    items: [MagicItem]
    monsters: [MagicMonster]
    world: str = "MAGIC"
