from collections import namedtuple
from itertools import repeat, chain
from random import choice, randint

from tcod.map import Map as TcodMap

Location = namedtuple('Location', ['x', 'y'])


class Tile:
    location: Location
    walkable: bool
    transparent: bool
    explored: bool

    def __init__(self, location, walkable=False, transparent=True):
        self.location = location
        self.walkable = walkable
        self.transparent = transparent
        self.explored = False

    @property
    def char(self):
        if not self.walkable and self.transparent:
            return " "
        elif self.walkable and self.transparent:
            return "."
        elif self.walkable and not self.transparent:
            return "#"


class Room:
    origin: Location
    tiles: [Tile]
    width: int
    height: int

    def __init__(self, origin: Location, width: int, height: int):
        x1 = origin.x
        x2 = origin.x + width + 1
        y1 = origin.y
        y2 = origin.y + height + 1
        self.origin = origin
        self.width = width
        self.height = height
        self.tiles = [[Tile(Location(x, y), walkable=True)
                       for x in range(x1, x2)]
                      for y in range(y1, y2)]


class Passage:
    origin: Location
    destination: Location
    tiles: [Tile]

    def __init__(self, origin: Location, dest: Room, direction: str):
        y2_range = list(range(dest.origin.y, dest.origin.y + dest.height + 1))
        x2_range = list(range(dest.origin.x, dest.origin.x + dest.width + 1))
        if dest.origin.x in x2_range:
            x2_range += list(repeat(origin.x, len(x2_range)))
        elif dest.origin.y in y2_range:
            y2_range += list(repeat(origin.y, len(y2_range)))

        if direction == 'D':
            i = 0
            p1 = (origin.x, origin.y + 1)
            p2 = (choice(x2_range), dest.origin.y - 1)
        elif direction == 'R':
            i = 1
            p1 = (origin.x + 1, origin.y)
            p2 = (dest.origin.x - 1, choice(y2_range))
        else:
            raise ValueError('Direction {} not correct'.format(direction))
        if p1[i] == p2[i]:
            self.straight_tiles(p1[0], p2[0], p1[1], p2[1])
        else:
            self.bent_tiles(p1, p2, i)

    def straight_tiles(self, x1, x2, y1, y2):
        self.tiles = [[Tile(Location(x, y), walkable=True, transparent=False)
                       for x in range(x1, x2)] for y in range(y1, y2)]

    def bent_tiles(self, p1, p2, i):
        if abs(p1[i] - p2[i]) > 2:
            bp = randint(min(p1[i], p2[i])+1,
                         max(p1[i], p2[i])-1)
        else:
            bp = p1[i] + 1
        self._walk_path(p1, p2, i, bp)
        i = 1 - i
        self._walk_path(p1, p2, i, p2[i])
        i = 1 - i
        self._walk_path(p1, p2, i, p2[i])

    def _walk_path(self, p1, p2, i, end):
        while p1[i] != end:
            self.tiles.append(Tile(Location(p1[0], p1[1]),
                                   walkable=True,
                                   transparent=False))
            if p1[i] < p2[i]:
                p1[i] += 1
            else:
                p1[i] -= 1
                print("MAKING PATH, DID NEED THIS")


class Map(TcodMap):

    def __init__(self, width, height, tiles, rooms, passages):
        super().__init__(width, height)
        self.tiles = tiles
        self.rooms = rooms
        self.passages = passages
        self.update_c_map()

    def update_c_map(self):
        for tile in chain(*self.tiles):
            x, y = tile.location
            self.walkable[y][x] = tile.walkable
            self.transparent[y][x] = tile.transparent
