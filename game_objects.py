import uuid

import pygame.sprite


class GameObject(pygame.sprite.Sprite):

    def __init__(self, x, y, world, image, active=True):
        super().__init__(world)
        self.world = world
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = active
        self.id = uuid.uuid4()

    def update(self):
        pass

    def collide(self, obj):
        pass

    def render(self, camera, screen):
        if not self.active:
            return
        screen.blit(self.image, (camera.x, camera.y))

    def is_inside(self, point):
        return self.image.get_bounding_rect().collidepoint(point[0], point[1])


class Entity(GameObject):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy


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

