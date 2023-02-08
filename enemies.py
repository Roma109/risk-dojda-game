import random

import pygame.math

from game_objects import Creature, FadingText, Entity
from player import Human, Item, ChargedWeapon
from world import CollideableTile


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


class BossEnemy(Enemy):
    def __init__(self, x, y, world, image, key, maxhp=200):
        super().__init__(x, y, world, image, key, maxhp)
        self.contact_damage = 3
        self.speed = 3
        self.jump_power = 6
        self.target_finder = HumanTargetFinder()
        self.target = self.target_finder.find_target(self)
        self.weapon = ChargedWeapon(3, 1000, self.target, self)
        self.delta_x = 0

    def update(self):
        if self.weapon.charge_amount <= 60:
            self.weapon.charge()
        else:
            self.weapon.shoot_charged()
        if self.delta_x < -15:
            self.direction = (1, 0)
        if self.delta_x > 15:
            self.direction = (-1, 0)
        self.delta_x += self.direction[0] * self.speed
        super().update()

    def kill(self):
        super().kill()
        self.world.add_object(Item(self.rect.centerx - 5, self.rect.centery, self.world, type='goal'))
        self.world.add_object(Item(self.rect.centerx + 5, self.rect.centery, self.world, type='all_stats'))


class HumanTargetFinder:

    def find_target(self, entity):
        return entity.world.player


class SpawnerTile(CollideableTile, Entity):

    def __init__(self, x, y, world, image, key):
        super().__init__(x, y, world, image, key)
        self.counter = 0
        self.gravity = False

    def collide(self, entity):
        super().collide(entity)
        if isinstance(entity, Human):
            self.initiate()
            BossEnemy(self.rect.x, self.rect.y, self.world, pygame.image.load('assets/enemies/hitscan-wisp.png'), 1)

    def initiate(self):
        self.counter += 1
        if self.counter % 10 == 0:
            FadingText(self.rect.x, self.rect.y + 16, self.world, str(4 - self.counter // 10), (255, 50, 50))
            if self.counter >= 30:
                BossEnemy(self.rect.x, self.rect.y, self.world, pygame.image.load('assets/enemies/hitscan-wisp.png'), 1)
                # self.world.remove_object(self)
                self.counter = -2000
