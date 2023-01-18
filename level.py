import pygame

import world
from world import World, Tile, Platform
from game_objects import GameObject


class Level:

    def __init__(self, world, start_pos):
        self.world = world
        self.start_pos = start_pos

    def update(self):
        self.world.update()


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
                w.add_object(GameObject(x * world.TILE_SIZE, y * world.TILE_SIZE, w,
                                      pygame.image.load('assets/level1/background_tile.png')))
            if elem == "B":
                w.add_tile(Tile(w, x, y, pygame.image.load('assets/level1/tile.png')))
            elif elem == "-":
                w.add_object(Platform(x * world.TILE_SIZE, y * world.TILE_SIZE, w,
                                      pygame.image.load('assets/level1/platform.png')))
            elif elem == "P":
                start_pos = (x * world.TILE_SIZE, y * world.TILE_SIZE)
                w.add_object(GameObject(x * world.TILE_SIZE, y * world.TILE_SIZE, w,
                                      pygame.image.load('assets/level1/player_start_point1.png')))
    return Level(w, start_pos)
