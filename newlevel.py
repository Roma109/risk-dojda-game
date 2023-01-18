import pygame
import pytmx

import world
from game_objects import Platform
from world import World, Tile

START_POSS = [(), (3, 10)]


class Level:
    global START_POSS

    def __init__(self, game, levelnumber):
        self.world = World()
        self.world.map = pytmx.load_pygame(f'assets/level{levelnumber}/map1.tmx')
        self.start_pos = START_POSS[levelnumber]
        self.height = self.world.map.height
        self.width = self.world.map.width
        self.tile_size = self.world.map.tilewidth
        start_pos = (0, 0)
        for y in range(self.height):
            for x in range(self.width):
                image = self.world.map.get_tile_image(x, y, 0)
                self.world.add_tile(Tile(self.world, x, y, image))
        self.start_pos = start_pos

    def update(self):
        self.world.update()
