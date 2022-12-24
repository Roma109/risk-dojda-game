import uuid
from typing import Any

import pygame.sprite


class GameObject(pygame.sprite.Sprite):

    def __init__(self, x, y, world, image, active=True):
        super().__init__(world.sprites_group)
        self.world = world
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = active
        self.id = uuid.uuid4()

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass

    def render(self, camera, screen):
        if not self.active:
            return
        screen.blit(self.image, (10, 10))

    def is_inside(self, point):
        return self.image.get_bounding_rect().collidepoint(point[0], point[1])


class Tickable(GameObject):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)

    def tick(self):
        pass


class Entity(Tickable):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)

    def collide(self):
        pass


class Creature(Entity):

    def __init__(self, x, y, world, image, hp, maxhp):
        super().__init__(x, y, world, image)
        self.hp = hp
        self.maxhp = maxhp

    def damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.kill()

    def kill(self):
        self.world.remove_object(self)

