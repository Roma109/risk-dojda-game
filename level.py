import random

import pygame

import world
from enemies import Enemy
from world import World, Tile, Platform
from game_objects import GameObject


class Level:

    def __init__(self, world, start_pos):
        self.world = world
        self.start_pos = start_pos
        self.enemies = []

    def update(self):
        if not self.enemies:
            enemy = Enemy(64, 64, self.world, pygame.image.load("assets/player.jpg"), 10, 10)
            self.world.add_object(enemy)
            self.enemies.append(enemy)
        self.world.update()
        for enemy in list(self.enemies):
            if not enemy.active:
                self.enemies.remove(enemy)



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


def generate_random_level(width, height):
    w = World()
    start_pos = None
    for y in range(height):
        platform_width = 0
        for x in range(width):
            if y != 0 and y != height - 1 and x != 0 and x != width - 1:
                if y > 1 and platform_width == 0 and random.random() > 0.9:
                    platform_width = random.randint(1, 5)
                if platform_width and w.get_obj((x * world.TILE_SIZE, (y - 1) * world.TILE_SIZE)) is None:
                    w.add_object(Platform(x * world.TILE_SIZE, y * world.TILE_SIZE, w,
                                          pygame.image.load('assets/level1/tile.png')))
                    platform_width -= 1
                    if start_pos is None:
                        start_pos = (x, y - 1)
            else:
                w.add_tile(Tile(w, x, y, pygame.image.load('assets/level1/tile.png')))
    print("OBJECTS=" + str(len(w.game_objects) + len(w.tiles)))
    return Level(w, start_pos)