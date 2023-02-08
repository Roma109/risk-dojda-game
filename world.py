import math

import pygame

import game_objects
import object_types
from camera import Camera
from game_objects import GameObject, Collideable


TILE_SIZE = 32


def distance_squared(pos1, pos2):
    return (pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2


def distance(pos1, pos2):
    return math.sqrt(distance_squared(pos1, pos2))


class World:

    def __init__(self, name, camera=None):
        if camera is None:
            camera = Camera()
        self.name = name
        self.game_objects = dict()
        self.tiles = dict()
        self.player = None
        self.camera = camera
        self.collideables = []
        self.background = None
        self.types = object_types.ObjectTypes()

    def register_type(self, object_type):
        self.types.register(object_type)

    def get(self, pos):
        obj = self.get_obj(pos)
        if obj is None:
            return self.get_tile(pos)
        else:
            return obj

    def add(self, obj):
        if isinstance(obj, Tile):
            self.add_tile(obj)
        #elif isinstance(obj, Human):
            #self.add_human(obj)
        else:
            self.add_object(obj)

    def get_obj(self, pos):
        objects = []
        for obj in self.game_objects.values():
            if obj.is_inside(pos):
                objects.append(obj)
        return objects[0] if len(objects) != 0 else None

    def add_object(self, obj: GameObject):
        self.game_objects[obj.id] = obj
        if isinstance(obj, Collideable):
            self.collideables.append(obj)

    def remove_object(self, obj: GameObject):
        del self.game_objects[obj.id]
        if isinstance(obj, Collideable):
            self.collideables.remove(obj)

    def set_player(self, player):
        self.add_object(player)
        self.player = player

    def add_tile(self, tile):
        self.tiles[tile.get_pos()] = tile
        if isinstance(tile, Collideable):
            self.collideables.append(tile)

    def get_tile(self, pos):
        for tile in self.tiles.values():
            if tile.is_inside(pos):
                return tile
        return None

    def raytrace(self, origin, direction, step=5, max_distance=100, conditions=None):
        if conditions is None:
            conditions = []
        step_x = direction[0] * step
        step_y = direction[1] * step
        pos = [origin[0], origin[1]]
        # distance_squared дешевле чем distance
        while distance_squared(origin, pos) < max_distance ** 2:
            pos[0] += step_x
            pos[1] += step_y
            obj = self.get((int(pos[0]), int(pos[1])))
            if obj is None or not isinstance(obj, Collideable):
                print(obj)
                continue
            fits = True
            for condition in conditions:
                if not condition(obj):
                    fits = False
                    break
            if fits:
                return RayTraceResult(obj, isinstance(obj, Tile), not isinstance(obj, Tile), origin, (int(pos[0]), int(pos[1])))
        return RayTraceResult(None, False, False, origin, (int(pos[0]), int(pos[1])))

    def update(self):
        self.camera.tick()
        for obj in list(self.game_objects.values()):
            obj.update()
        self.calculate_intersections()

    def calculate_intersections(self):
        for i in range(len(self.collideables) - 1):
            for j in range(i + 1, len(self.collideables)):
                # TODO: убрать трай кетч
                # скорее всего ошибка вылезает потому что какой-то обьект пропадает из self.collidables
                # во время коллизии
                # надо вообще в world.update() неактивные обьекты удалять, нельзя чтобы они сами удалялись
                try:
                    first = self.collideables[i]
                    second = self.collideables[j]
                    if first.rect.colliderect(second.rect):
                        first.collide(second)
                        second.collide(first)
                except IndexError as e:
                    print(e)

    def render(self, screen):
        if self.background:
            screen.blit(self.background.image, self.background.rect)
        for tile in self.tiles.values():
            tile.draw(self.camera, screen)
        for obj in self.game_objects.values():
            obj.draw(self.camera, screen)


class RayTraceResult:

    def __init__(self, obj, hit_tile, hit_object, origin, end):
        self.obj = obj
        self.hit_tile = hit_tile
        self.hit_object = hit_object
        self.origin = origin
        self.end = end


class Tile(GameObject):

    def __init__(self, x, y, world, image, key):
        super().__init__(x * TILE_SIZE, y * TILE_SIZE, world, image, key)
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def is_saveable(self):
        return False


class CollideableTile(Tile, Collideable):

    def __init__(self, x, y, world, image, key):
        super().__init__(x, y, world, image, key)

    def collide(self, entity):
        if not isinstance(entity, game_objects.Entity):
            return
        if entity.rect.collidepoint(self.rect.midtop):
            # обьект касается верхней стороны тайла
            if entity.vy > 0:
                entity.vy = 0
            entity.rect.bottom = self.rect.top
            entity.on_ground = 2
        if entity.rect.collidepoint(self.rect.midright):
            # обьект касается правой стороны тайла
            if entity.vx > 0:
                entity.vx = 0
            entity.rect.left = self.rect.right
        if entity.rect.collidepoint(self.rect.midbottom):
            # нижней стороны
            if entity.vy < 0:
                entity.vy = 0
            entity.rect.top = self.rect.bottom
        if entity.rect.collidepoint(self.rect.midleft):
            # левой стороны
            if entity.vx < 0:
                entity.vx = 0
            entity.rect.right = self.rect.left


class Platform(GameObject, Collideable):

    def __init__(self, x, y, world, image, key):
        super().__init__(x, y, world, image, key)
        self.key = key

    def collide(self, entity):
        if not isinstance(entity, game_objects.Entity):
            return
        height = entity.rect.clip(self.rect).height
        if height / (entity.vy if entity.vy != 0 else 1) <= 1:
            if entity.rect.collidepoint(self.rect.midtop) or \
                    entity.rect.collidepoint(self.rect.topright) or \
                    entity.rect.collidepoint(self.rect.topleft):
                if entity.direction[1] <= 0 <= entity.vy:
                    entity.vy = 0
                    entity.on_ground = 2
                    entity.rect.bottom = self.rect.top

    def is_saveable(self):
        return False


class Background:

    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()
