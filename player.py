import pygame

from game_objects import Creature


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


class Control:  # управление игроком

    def __init__(self):
        # управление
        self.buttons = dict()

    def save_defaults(self):
        self.buttons[pygame.K_LEFT] = MoveAction((-1, 0))
        self.buttons[pygame.K_UP] = MoveAction((0, -1))
        self.buttons[pygame.K_RIGHT] = MoveAction((1, 0))
        self.buttons[pygame.K_DOWN] = MoveAction((0, 1))

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
