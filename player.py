import pygame

import world
from game_objects import Creature, GameObject


class Weapon:

    def __init__(self):
        self.range = 1000
        self.damage = 10

    def shoot(self, who, origin, direction):
        ray_trace_result = who.world.raytrace(origin, direction,
                                              max_distance=self.range,
                                              conditions=[lambda obj: obj != who,
                                                          lambda obj: not isinstance(obj, world.Platform)])
        who.world.add_object(WeaponTrace(origin, ray_trace_result.end, who.world,
                                         time=2, width=3, color=(100, 255, 100)))
        if ray_trace_result.hit_object and isinstance(ray_trace_result.obj, Creature):
            ray_trace_result.obj.damage(self.damage)


class WeaponTrace(GameObject):

    def __init__(self, origin, target, w, time=20, width=5, color=None):
        super().__init__(origin[0], origin[1], w,
                         pygame.Surface((1000, 1000)))
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
    # использовался бы в мультиплеере, может стоит выпилить
    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image, 10, 10)


class Player(Human):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)
        self.speed = 10
        self.control = Control()
        self.control.save_defaults()
        self.feet = (self.rect.bottomleft, self.rect.midbottom, self.rect.bottomright)
        self.weapon = Weapon()

    def shoot(self, direction):
        self.weapon.shoot(self, self.get_pos(), direction)


class Control:  # управление игроком

    def __init__(self):
        # управление
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

    def __init__(self, direction):  # direction - кортеж с направлениями по x и y - числами от 0 до 1
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

# оно не работает
#class PauseAction(Action):
#
#    def start(self, player):
#        main.get_game().state.next_state = lambda game, prev_state: main.GamePauseState(game, prev_state)
