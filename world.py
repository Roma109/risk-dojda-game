import pygame.sprite

from camera import Camera
from game_objects import GameObject
from player import Human


TILE_SIZE = 32


class World(pygame.sprite.Group):

    def __init__(self, camera=None):
        super().__init__()
        if camera is None:
            camera = Camera()
        self.game_objects = dict()
        self.tiles = dict()
        self.humans = []
        self.camera = camera

    def get_obj(self, pos):
        objects = []
        for obj in self.game_objects.values():
            if obj.is_inside(pos):
                objects.append(obj)
        filter(lambda x: x.priority, objects)
        return objects[0] if len(objects) != 0 else None

    def add_object(self, obj: GameObject):
        self.game_objects[obj.id] = obj
        self.add(obj)

    def remove_object(self, obj: GameObject):
        del self.game_objects[obj.id]
        self.remove(obj)

    def add_human(self, human: Human):
        self.humans.append(human)
        self.add_object(human)

    def remove_human(self, human: Human):
        self.humans.remove(human)
        self.remove_object(human)

    def add_tile(self, tile):
        self.tiles[tile.get_pos()] = tile
        self.add(tile)

    def update(self):
        self.camera.tick()
        for obj in list(self.game_objects.values()):
            obj.update()
            self.camera.apply(obj)
        for tile in self.tiles.values():
            self.camera.apply(tile)
        intersections = pygame.sprite.groupcollide(self, self, False, False)
        for obj in intersections:
            for other in intersections[obj]:
                if obj == other:
                    continue
                obj.collide(other)


class Tile(pygame.sprite.Sprite):

    def __init__(self, world, x, y, image):
        super().__init__(world)
        self.world = world
        self.x = x
        self.y = y
        self.rect = image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.image = image

    def get_pos(self):
        return self.x, self.y

    def collide(self, entity):
        print(f'self={self}, entity={entity}')
        if entity.rect.collidepoint(self.rect.midtop) or \
            entity.rect.collidepoint(self.rect.topleft) or \
                entity.rect.collidepoint(self.rect.topright):
            # обьект касается верхней стороны тайла
            if entity.vy < 0:
                entity.vy = 0
            entity.on_ground = True
        if entity.rect.collidepoint(self.rect.topright) or \
            entity.rect.collidepoint(self.rect.right) or \
                entity.rect.collidepoint(self.rect.bottomright):
            # обьект касается правой стороны тайла
            if entity.vx > 0:
                entity.vx = 0
        if entity.rect.collidepoint(self.rect.topright) or \
                entity.rect.collidepoint(self.rect.right) or \
                entity.rect.collidepoint(self.rect.bottomright):
            # нижней стороны
            if entity.vy > 0:
                entity.vy = 0
        if entity.rect.collidepoint(self.rect.topright) or \
                 entity.rect.collidepoint(self.rect.right) or \
                 entity.rect.collidepoint(self.rect.bottomright):
            # левой стороны
            if entity.vx < 0:
                entity.vx = 0
