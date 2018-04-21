from collections import namedtuple
from itertools import chain, permutations
from random import choice, randint, randrange, shuffle

import networkx as nx
from tcod.map import Map as TcodMap

from src.maps.config import MAP_WIDTH, MAP_HEIGHT
from src.maps.config import MIN_ROOM_W, MAX_ROOM_W, MIN_ROOM_H, MAX_ROOM_H
from src.maps.mazes import get_maze

Location = namedtuple('Location', ['x', 'y'])


class Tile:
    location: Location
    walkable: bool
    transparent: bool
    hidden: bool
    explored: bool

    def __init__(self, location, walkable=False, transparent=False):
        self.location = location
        self.walkable = walkable
        self.transparent = transparent
        self.explored = True # False
        self.hidden = False

    @property
    def char(self):
        if not self.walkable and self.transparent:
            return " "
        elif self.walkable and self.transparent:
            return "."
        elif self.walkable and not self.transparent:
            return "#"

    def __repr__(self):
        return "Tile x:{}, y{}, w: {}, t: {}".format(self.location.x,
                                                     self.location.y,
                                                     self.walkable,
                                                     self.transparent)


class Room:
    origin: Location
    tiles: [[Tile]]
    width: int
    height: int
    doors: dict

    def __init__(self, origin: Location, width: int, height: int):
        x1 = origin.x
        x2 = origin.x + width + 1
        y1 = origin.y
        y2 = origin.y + height + 1
        self.origin = origin
        self.width = width
        self.height = height
        self.tiles = [[Tile(Location(x, y), walkable=True, transparent=True)
                       for x in range(x1, x2)]
                      for y in range(y1, y2)]
        self.doors = dict(TOP=None,
                          BOTTOM=None,
                          LEFT=None,
                          RIGHT=None
                          )


class Passage:
    origin: Location
    destination: Location
    tiles: [Tile]

    def __init__(self, origin: Location, dest: Location, direction: str):
        if direction == 'TB':
            i = 1
            p1 = (origin.x, origin.y + 1)
            p2 = (dest.x, dest.y)
        elif direction == 'LR':
            i = 0
            p1 = (origin.x + 1, origin.y)
            p2 = (dest.x, dest.y)
        else:
            raise ValueError('Direction {} not correct'.format(direction))
        if p1[i] == p2[i]:
            self.straight_tiles(p1[0], p2[0], p1[1], p2[1])
        else:
            self.bent_tiles(p1, p2, i)

    def straight_tiles(self, x1, x2, y1, y2):
        self.tiles = [Tile(Location(x, y), walkable=True, transparent=False)
                      for x in range(x1, x2+1) for y in range(y1, y2+1)]

    def bent_tiles(self, p1, p2, i):
        p1 = list(p1)
        if abs(p1[i] - p2[i]) > 2:
            bp = randint(min(p1[i], p2[i])+1,
                         max(p1[i], p2[i])-2)
        else:
            bp = p1[i] + 1
        self.tiles = []
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
            if p1[i] < end:
                p1[i] += 1
            else:
                p1[i] -= 1


class Map(TcodMap):

    def __init__(self, lvl_num):
        # Rooms in 3x3 grid:
        # 0 1 2
        # 3 4 5
        # 6 7 8

        # Utilities for generating parameters
        self._grid_x_bounds = [1, MAP_WIDTH//3, MAP_WIDTH*2//3, MAP_WIDTH-1]
        self._grid_y_bounds = [1, MAP_HEIGHT//3, MAP_HEIGHT*2//3, MAP_HEIGHT-1]
        ltr = dict(d="LR")
        ttb = dict(d="TB")
        self._room_network = [(0, 1, ltr), (0, 3, ttb), (1, 4, ttb),
                              (1, 2, ltr), (2, 5, ttb), (3, 4, ltr),
                              (3, 6, ttb), (4, 5, ltr), (4, 7, ttb),
                              (5, 8, ttb), (6, 7, ltr), (7, 8, ltr)]
        self._graph = nx.Graph()
        self._graph.add_edges_from(self._room_network)
        rmb = [(0, 1), (1, 2), (2, 3)]
        self._room_bounds = [[a, b] for b in rmb for a in rmb]

        # Interface parameters
        super().__init__(MAP_WIDTH, MAP_HEIGHT)
        self.tiles = [[Tile(Location(x, y)) for x in range(MAP_WIDTH)]
                      for y in range(MAP_HEIGHT)]
        self.gen_rooms()
        self.gen_passages()
        if lvl_num > 4:
            self.remove_room(0)
            self.gen_maze()
            self.hide_tiles()
        else:
            self.remove_room(5-lvl_num)
        self.make_rooms()
        self.make_passages()
        self.update_c_map()

    def update_c_map(self):
        """Make tcods map the same as the tiles"""
        for tile in chain(*self.tiles):
            x, y = tile.location
            self.walkable[y][x] = tile.walkable
            self.transparent[y][x] = tile.transparent

    def gen_rooms(self):
        """Place the rooms, one in each of the sections"""
        self.rooms = [self._place_room(self._bound_to_coords(bound))
                      for bound in self._room_bounds]

    def gen_passages(self):
        """Use a spanning tree to connect the rooms,
        add a couple more paths for loops and variety."""
        search_method = choice([nx.dfs_edges, nx.bfs_edges])
        starting_room = randrange(0, len(self.rooms))
        connections = list(search_method(self._graph, starting_room))
        self.passages = [self._connect(c) for c in connections]
        excluded = [(x, y) for x, y, z in self._room_network
                    if (x, y) not in connections]
        extras = set([choice(excluded) for _ in range(randint(1, 5))])
        self.passages += [self._connect(c) for c in extras]

    def make_passages(self):
        for pt in chain(*[p.tiles for p in self.passages]):
            tile = self.tiles[pt.location.y][pt.location.x]
            assert(tile.location == pt.location)
            tile.walkable = pt.walkable
            tile.transparent = pt.transparent
            tile.hidden = pt.hidden

    def make_rooms(self):
        for t in chain(*chain(*[room.tiles for room in self.rooms])):
            tile = self.tiles[t.location.y][t.location.x]
            assert(tile.location == t.location)
            tile.walkable = t.walkable
            tile.transparent = t.transparent

    def _bound_to_coords(self, bound):
        """Given a bounding region, return the coords
        that define that region."""
        return [(self._grid_x_bounds[bound[0][0]],
                 self._grid_x_bounds[bound[0][1]]),
                (self._grid_y_bounds[bound[1][0]],
                 self._grid_y_bounds[bound[1][1]])]

    def _place_room(self, coords):
        """Given bounding coords for a grid section,
        return a room that is within that section."""
        (minx, maxx), (miny, maxy) = coords
        minx += 1
        maxx -= 2
        miny += 1
        maxy -= 2
        width = randint(MIN_ROOM_W, MAX_ROOM_W)
        height = randint(MIN_ROOM_H, MAX_ROOM_H)
        maxx -= width
        maxy -= height
        x = maxx if maxx == minx else randint(minx+1, maxx)
        y = maxy if maxy == miny else randint(miny+1, maxy)
        return Room(Location(x, y), width, height)

    def _connect(self, connect):
        """Given two room numbers to connect, return a Passage
        that connects them."""
        direction = self._graph[min(connect)][max(connect)]['d']
        room1 = self.rooms[min(connect)]
        room2 = self.rooms[max(connect)]
        if direction == "LR":
            default = choice([row[-1] for row in room1.tiles][1:-1])
            origin = self._choose_door(room1, "RIGHT", default)
            dest = self._choose_dest(origin, room2, "LEFT")
        elif direction == "TB":
            default = choice(room1.tiles[-1][1:-1])
            origin = self._choose_door(room1, "BOTTOM", default)
            dest = self._choose_dest(origin, room2, "TOP")
        return Passage(origin=origin.location,
                       dest=dest.location,
                       direction=direction)

    def _choose_door(self, room, side, default):
        if room.doors[side] is None:
            room.doors[side] = default
            return default
        else:
            return room.doors[side]

    def _choose_dest(self, origin, room, side):
        if room.doors[side] is not None:
            return room.doors[side]
        elif side == "TOP":
            if randint(1, 10) < 5:
                for t in room.tiles[0]:
                    if origin.location.x == t.location.x:
                        room.doors[side] = t
                        return t
            door = choice(room.tiles[0][1:-1])
            room.doors[side] = door
            return door
        elif side == "LEFT":
            if randint(1, 10) < 5:
                for t in [r[0] for r in room.tiles]:
                    if origin.location.y == t.location.y:
                        room.doors[side] = t
                        return t
            door = choice([r[0] for r in room.tiles][1:-1])
            room.doors[side] = door
            return door

    def remove_room(self, chance):
        rooms_with_two_doors = [rm for rm in self.rooms
                                if len([d for d in rm.doors.values()
                                        if d is not None]) == 2]

        if len(rooms_with_two_doors) > 0 and randint(1, 10) < 4 - chance:
            self._remove_room(choice(rooms_with_two_doors), chance)

    def _remove_room(self, rm, chance):
        if rm.doors["LEFT"] is not None:
            direction = "LR"
            d1 = rm.doors["LEFT"]
            d1.location = Location(d1.location.x - 1, d1.location.y)
        elif rm.doors["TOP"] is not None:
            direction = "TB"
            d1 = rm.doors["TOP"]
            d1.location = Location(d1.location.x, d1.location.y - 1)
        elif rm.doors["RIGHT"] is not None:
            direction = "TB"
            d1 = rm.doors["RIGHT"]
            d1.location = Location(d1.location.x + 1, d1.location.y)
        side, d2 = [(s, d) for s, d in rm.doors.items()
                    if d != d1 and d is not None][0]
        if side == "TOP":
            d2.location = Location(d2.location.x, d2.location.y - 1)
        elif side == "RIGHT":
            d2.location = Location(d2.location.x + 1, d2.location.y)
        elif side == "BOTTOM":
            d2.location = Location(d2.location.x, d2.location.y + 1)
        self.passages.append(Passage(d1.location, d2.location, direction))
        self.rooms.remove(rm)
        self.remove_room(chance + 1)

    def gen_maze(self):
        potential_rooms = [rm for rm in self.rooms
                           if rm.width > 8 and
                           rm.height > 6
                           ]
        if len(potential_rooms) > 0 and randint(0, 10) < 3:
            self.make_maze(choice(potential_rooms))

    def make_maze(self, rm):
        maze = get_maze(rm.width+1, rm.height+1)
        if rm.doors["TOP"] is not None:
            loc = rm.doors["TOP"].location
            x = loc.x - rm.origin.x
            maze[0][x] = 1
        if rm.doors["BOTTOM"] is not None:
            loc = rm.doors["BOTTOM"].location
            x = loc.x - rm.origin.x
            maze[-1][x] = 1
        if rm.doors["LEFT"] is not None:
            loc = rm.doors["LEFT"].location
            y = loc.y - rm.origin.y
            maze[y][0] = 1
        if rm.doors["RIGHT"] is not None:
            loc = rm.doors["RIGHT"].location
            y = loc.y - rm.origin.y
            maze[y][-1] = 1

        for mrow, trow in zip(maze, rm.tiles):
            for m, tile in zip(mrow, trow):
                if m == 0:
                    tile.walkable = False
                tile.transparent = False

    def hide_tiles(self):
        for _ in range(randint(0, 4)):
            to_door = randint(-1, 1)
            if to_door != 1:
                tile = choice(self.passages).tiles[to_door]
            else:
                tile = choice(list(chain(*[p.tiles for p in self.passages])))
            tile.hidden = True
            tile.transparent = False
            tile.walkable = False
