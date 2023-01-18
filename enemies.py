import pygame.math

import world
from game_objects import Creature
from player import Human


class EntitySentient(Creature):

    def __init__(self, x, y, w, image, hp, maxhp, target_finder):
        super().__init__(x, y, w, image, hp, maxhp)
        self.target_finder = target_finder
        self.target = None

    def update(self):
        if self.target is None:
            self.target = self.target_finder.find_target(self)
        if self.target is not None:
            vector_direction = pygame.math.Vector2(self.rect.x - self.target.rect.x,
                                                   self.rect.y - self.target.rect.y)
            self.direction = (-vector_direction.x / vector_direction.length(), -vector_direction.y / vector_direction.length())
        super().update()

    def set_target(self, target):
        self.target = target


class Enemy(EntitySentient):

    def __init__(self, x, y, world, image, hp, maxhp):
        super().__init__(x, y, world, image, hp, maxhp, HumanTargetFinder())
        self.contact_damage = 2
        self.speed = 5
        self.jump_power = 10

    def collide(self, other):
        if isinstance(other, Human):
            other.damage(self.contact_damage)


class HumanTargetFinder:

    def find_target(self, entity):
        humans = list(filter(lambda x: world.distance_squared(entity.get_pos(), x.get_pos()),
                             entity.world.humans))
        return humans[0] if humans else None
