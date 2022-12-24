import pygame.sprite

from game_objects import GameObject
from player import Human


class World(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.game_objects = dict()
        self.humans = []

    def get_obj(self, pos):
        for obj in self.game_objects.values():
            if obj.is_inside(pos):
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

    def render(self, screen, camera):
        # TODO: добавить бекграунд
        for sprite in self.sprites():
            sprite.render(camera, screen)

    def draw(self, surface):
        # вызов этого метода эквивалентен рендеру с камерой по координатам 0, 0
        raise NotImplementedError('use world.render(screen, camera)')

    def update(self):
        for obj in list(self.game_objects.values()):
            obj.update()

