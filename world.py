import pygame.sprite

from camera import Camera
from game_objects import GameObject
from player import Human


class World(pygame.sprite.Group):

    def __init__(self, camera=None):
        super().__init__()
        if camera is None:
            camera = Camera()
        self.game_objects = dict()
        self.humans = []
        self.camera = camera

    def get_obj(self, pos):
        for obj in self.game_objects.values():
            if obj.is_inside(pos) and obj.priority >= 0:
                return obj

    def add_object(self, obj: GameObject):
        self.game_objects[obj.id] = obj
        self.add(obj)

    def remove_object(self, obj: GameObject):
        del self.game_objects[obj.id]
        self.remove(obj)

    def add_human(self, human: Human):
        self.humans.append(human)
        self.add(human)

    def remove_human(self, human: Human):
        self.humans.remove(human)
        self.remove(human)

    def update(self):
        for obj in list(self.game_objects.values()):
            obj.update()
            self.camera.apply(obj)

