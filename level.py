import random

import pygame

import world
from enemies import Enemy
from player import Human
from world import World, Tile, CollideableTile, Platform, GameObject


class Level(World):

    def __init__(self, start_pos=None):
        super().__init__()
        if start_pos is None:
            start_pos = (0, 0)
        self.start_pos = start_pos
        self.enemies = []

    def add_human(self, human: Human):
        super().add_human(human)
        human.rect.x = self.start_pos[0]
        human.rect.y = self.start_pos[1]

    def update(self):
        if not self.enemies:
            enemy_sprite = pygame.transform.scale(pygame.image.load("assets/enemies/hitscan-wisp.png"), (32, 32))
            enemy = Enemy(64, 64, self, enemy_sprite, 10, 10)
            self.add_object(enemy)
            self.enemies.append(enemy)
        super().update()
        for enemy in list(self.enemies):
            if not enemy.active:
                self.enemies.remove(enemy)


def load_level():
    map = ['B                                                                                            B',
           'B                                                                                            B',
           'B                                       -------                                              B',
           'B        ------                                          -----                               B',
           'B   --                    ---------                ---                                       B',
           'B                                           P                                                B',
           'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB']
    w = Level()
    for y in range(len(map)):
        row = map[y]
        for x in range(len(row)):
            elem = row[x]
            if elem == " ":
                w.add_tile(Tile(x, y, w,
                                pygame.image.load('assets/level1/background_tile.png')))
            elif elem == "B":
                w.add_tile(CollideableTile(x, y, w, pygame.image.load('assets/level1/platform.png')))
            elif elem == "-":
                w.add_object(Platform(x * world.TILE_SIZE, y * world.TILE_SIZE, w,
                                      pygame.image.load('assets/level1/platform.png')))
            elif elem == "P":
                w.start_pos = (x * world.TILE_SIZE, y * world.TILE_SIZE)
                w.add_object(GameObject(x * world.TILE_SIZE, y * world.TILE_SIZE,
                                        w, pygame.image.load('assets/level1/player_start_point.png')))
    return w


def generate_random_level(width, height):
    w = Level()
    start_pos = None
    for y in range(height):
        platform_width = 0
        for x in range(width):
            if y != 0 and y != height - 1 and x != 0 and x != width - 1:
                if y > 1 and platform_width == 0 and random.random() > 0.9:
                    platform_width = random.randint(1, 5)
                if platform_width and w.get_obj((x * world.TILE_SIZE, (y - 1) * world.TILE_SIZE)) is None:
                    w.add_object(Platform(x * world.TILE_SIZE, y * world.TILE_SIZE, w,
                                          pygame.image.load('assets/level1/platform.png')))
                    platform_width -= 1
                    if start_pos is None:
                        start_pos = (x, y - 1)
            else:
                w.add_tile(CollideableTile(w, x, y, pygame.image.load('assets/level1/tile.png')))
    print("OBJECTS=" + str(len(w.game_objects) + len(w.tiles)))
    return w
