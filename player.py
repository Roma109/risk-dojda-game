import pygame
import random
import world
from game_objects import Creature, GameObject, Entity, FadingText, Updateable
import game_over

ITEM_PROPERTIES = {'damage': ('assets/items/damage.png', 'Damage up!', (200, 60, 60)),
                   'range': ('assets/items/range.png', 'Range up!', (60, 200, 60)),
                   'speed': ('assets/items/speed.png', 'Speed up!', (60, 60, 200)),
                   'all_stats': ('assets/items/pearl.png', 'All stats up!!!', (255, 255, 255)),
                   'goal': ('assets/items/fuel.png', 'Fuel obtained!', (255, 255, 255))}
ITEM_TYPES = ['damage', 'speed', 'range', 'all_stats', 'goal']


class Weapon:

    def __init__(self, damage, range):
        self.range = range
        self.damage = damage

    def shoot(self, who, origin, direction, beam_width=3):
        ray_trace_result = who.world.raytrace(origin, direction,
                                              max_distance=self.range, conditions=[lambda obj: obj != who,
                                                                                   lambda obj: not isinstance(obj,
                                                                                                              world.Platform)],
                                              except_classes=[WeaponTrace])
        who.world.add_object(
            WeaponTrace(origin, ray_trace_result.end, who.world, time=2, width=beam_width,
                        color=(min(10 * self.damage, 200),
                               max(255 - 10 * self.damage,
                                   80),
                               max(100 - 5 * self.damage,
                                   80))))
        if ray_trace_result.hit_object and isinstance(ray_trace_result.obj, Creature):
            ray_trace_result.obj.damage(self.damage)


class ChargedWeapon(Weapon):
    def __init__(self, damage, range, target, owner: Creature):
        super().__init__(damage, range)
        self.charge_amount = 0
        self.target = target
        self.owner = owner
        self.color = (0, 0, 0)
        self.beam_start = None
        self.beam_end = None
        self.vector = pygame.math.Vector2(0, 0)

    def charge(self):
        self.beam_start = self.owner.rect.centerx, self.owner.rect.centery
        self.beam_end = (self.target.rect.centerx, self.target.rect.centery)
        if self.charge_amount <= 50:
            self.vector = pygame.math.Vector2(self.target.rect.centerx - self.beam_start[0],
                                              self.target.rect.centery - self.beam_start[1]).normalize()
        self.color = (min(self.charge_amount + 140, 255), max(255 - self.charge_amount, 0), 85)
        if 50 >= self.charge_amount >= 15:
            self.owner.world.add_object(WeaponTrace(self.beam_start, self.beam_end, self.owner.world, time=0, width=2,
                                                    color=self.color))
        self.charge_amount += 1

    def shoot_charged(self):
        self.shoot(self.owner, self.beam_start, self.vector, beam_width=10)
        self.charge_amount = 0


class WeaponTrace(GameObject, Updateable):

    def __init__(self, origin, target, world, time=20, width=5, color=None):
        super().__init__(origin[0], origin[1], world,
                         pygame.Surface((1000, 1000)), None)
        if color is None:
            color = (255, 255, 255)
        self.origin = origin
        self.target = target
        self.image.set_colorkey((0, 0, 0))
        self.time = time
        pygame.draw.line(self.image, color, (origin[0] - self.rect.x, origin[1] - self.rect.y),
                         (target[0] - self.rect.x, target[1] - self.rect.y), width)

    def update(self):
        if self.time:
            self.time -= 1
        else:
            self.active = False
            self.world.remove_object(self)


class Human(Creature):
    # ?????????????????????????? ???? ?? ????????????????????????, ?????????? ?????????? ????????????????
    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image, None, 10, 10)


class Player(Human):

    def __init__(self, x, y, world, image, progress=0):
        super().__init__(x, y, world, image)
        self.base_speed = 10
        self.base_damage = 10
        self.base_range = 1000
        self.damage_multiplier = 1
        self.speed_multiplier = 1
        self.range_multiplier = 1
        self.control = Control()
        self.control.save_defaults()
        self.feet = (self.rect.bottomleft, self.rect.midbottom, self.rect.bottomright)
        self.weapon = Weapon(self.base_damage * self.damage_multiplier, self.base_range * self.range_multiplier)
        self.progress = progress

    def shoot(self, direction):
        self.weapon.shoot(self, self.get_pos(), direction)

    def get_item(self, type):
        if type == 'goal':
            self.progress += 1
        if type == 'speed':
            self.speed_multiplier += 0.2
            self.speed = min(self.base_speed * self.speed_multiplier, 20)
        else:
            if type == 'damage':
                self.damage_multiplier += 0.15

            if type == 'range':
                self.range_multiplier += 0.2
            if type == 'all_stats':
                self.range_multiplier *= 1.15
                self.damage_multiplier *= 1.15
                self.speed_multiplier *= 1.15
                self.speed = min(self.base_speed * self.speed_multiplier, 20)
            self.weapon = Weapon(round(self.base_damage * self.damage_multiplier),
                                 round(self.base_range * self.range_multiplier))
        self.maxhp += 1
        self.hp = max(self.hp + 2, self.maxhp)

    def recalc_stats(self):
        self.speed = min(self.base_speed * self.speed_multiplier, 20)
        self.weapon.damage = round(self.base_damage * self.damage_multiplier)
        self.weapon.range = round(self.base_range * self.range_multiplier)

    def save(self):
        data = super().save()
        data['progress'] = self.progress
        data['damage'] = self.damage_multiplier
        data['speed'] = self.speed_multiplier
        data['range'] = self.range_multiplier
        print(data)
        return data

    def apply(self, data):
        print(data)
        super().apply(data)
        self.progress = data['progress']
        self.damage_multiplier = data['damage']
        self.speed_multiplier = data['speed']
        self.range_multiplier = data['range']


class Control:  # ???????????????????? ??????????????

    def __init__(self):
        # ????????????????????
        self.buttons = dict()

    def save_defaults(self):
        self.buttons[pygame.K_a] = MoveAction((-1, 0))
        self.buttons[pygame.K_w] = MoveAction((0, -1))
        self.buttons[pygame.K_d] = MoveAction((1, 0))
        self.buttons[pygame.K_s] = MoveAction((0, 1))
        # self.buttons[pygame.K_ESCAPE] = PauseAction()

    def get_action(self, button):
        return self.buttons[button]

    def bind_action(self, button, action):
        self.buttons[button] = action


class Action:

    def start(self, player):
        pass

    def end(self, player):
        pass


class MoveAction(Action):

    def __init__(self, direction):  # direction - ???????????? ?? ?????????????????????????? ???? x ?? y - ?????????????? ???? 0 ???? 1
        self.direction = direction

    def start(self, player):
        dx, dy = player.direction
        if self.direction[0]:
            dx = self.direction[0]
        if self.direction[1]:
            dy = self.direction[1]
        player.direction = (dx, dy)

    def end(self, player):
        dx, dy = player.direction
        if dx == self.direction[0]:
            dx = 0
        if dy == self.direction[1]:
            dy = 0
        player.direction = (dx, dy)


class Item(Entity):
    global ITEM_PROPERTIES, ITEM_TYPES

    def __init__(self, x, y, world, type=None):
        if type is None:
            self.type = random.choices(ITEM_TYPES, weights=[25, 35, 30, 10, 0], k=1)[0]
        else:
            self.type = type
        image = pygame.image.load(ITEM_PROPERTIES[self.type][0])
        super().__init__(x, y, world, image, "item")

    def collide(self, other):
        if isinstance(other, Player) and self.active:
            other.get_item(self.type)
            self.active = False
            self.world.remove_object(self)
            if not self.type == 'goal':
                self.world.add_object(FadingText(self.rect.center[0], self.rect.center[1],
                                                 self.world, ITEM_PROPERTIES[self.type][1],
                                                 ITEM_PROPERTIES[self.type][2]))
            else:
                self.world.add_object(FadingText(self.rect.center[0], self.rect.center[1] - 32,
                                                 self.world, ITEM_PROPERTIES[self.type][1],
                                                 ITEM_PROPERTIES[self.type][2]))

    def save(self):
        data = super().save()
        data['item_type'] = self.type
        return data


class Rocket(Entity):
    def __init__(self, x, y, world, image, key, fuel_required=7):
        super().__init__(x, y, world, image, key, gravity=False)

    def collide(self, entity):
        super().collide(entity)
        if isinstance(entity, Player):
            if entity.progress >= 7:
                self.world.add_object(FadingText(self.rect.centerx, self.rect.centery, self.world, 'Ship Fueled. Taking off...'))
                entity.active = False
