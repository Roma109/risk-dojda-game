import pygame

import world
from game_objects import Platform
from world import World, Tile


class Level:

    def __init__(self, world, start_pos):
        self.world = world
        self.start_pos = start_pos

    def update(self, time):
        self.world.update(time)


def load_level():
    map = ['BBBBBBBBBB',
           'B        B',
           'B   - -  B',
           'B P      B',
           'B -   -  B',
           'B        B',
           'BBBBBBBBBB']
    w = World()
    start_pos = (0, 0)
    for y in range(len(map)):
        row = map[y]
        for x in range(len(row)):
            elem = row[x]
            if elem == " ":
                continue
            if elem == "B":
                w.add_tile(Tile(w, x, y, pygame.image.load('assets/level1/tile.png')))
            elif elem == "-":
                w.add_object(Platform(x * world.TILE_SIZE, y * world.TILE_SIZE, w,
                                      pygame.image.load('assets/level1/tile.png')))
            elif elem == "P":
                start_pos = (x * world.TILE_SIZE, y * world.TILE_SIZE)
    return Level(w, start_pos)
