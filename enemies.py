import random

import pygame.math

import world
from game_objects import Creature
from player import Human, Item


class EntitySentient(Creature):

    def __init__(self, x, y, w, image, key, hp, maxhp, target_finder):
        super().__init__(x, y, w, image, key, hp, maxhp)
        self.target_finder = target_finder
        self.target = None

    def update(self):
        if self.target is None:
            self.target = self.target_finder.find_target(self)
        if self.target is not None:
            vector_direction = pygame.math.Vector2(self.rect.x - self.target.rect.x,
                                                   self.rect.y - self.target.rect.y)
            if vector_direction.length():
                self.direction = (-vector_direction.x / vector_direction.length(),
                                  -vector_direction.y / vector_direction.length())
        super().update()

    def set_target(self, target):
        self.target = target


class Enemy(EntitySentient):

    def __init__(self, x, y, world, image, key, maxhp):
        super().__init__(x, y, world, image, key, maxhp, maxhp, HumanTargetFinder())
        self.contact_damage = 2
        self.speed = 5
        self.jump_power = 10

    def collide(self, other):
        if isinstance(other, Human):
            other.damage(self.contact_damage)

    def kill(self):
        super().kill()
        if random.random() > 0.8:
            self.world.add_object(Item(self.rect.centerx, self.rect.centery, self.world))


class HumanTargetFinder:

    def find_target(self, entity):
        return entity.world.player
