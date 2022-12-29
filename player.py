from game_objects import Creature
from camera import Camera, ObjectFollowMode


class Human(Creature):
# использовался бы в мультиплеере, может стоит выпилить
    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)


class Player(Human):

    def __init__(self, x, y, world, image, camera=None):
        super().__init__(x, y, world, image)
        if camera is None:
            camera = Camera()
        self.camera = camera
        self.camera.mode = ObjectFollowMode(self)
        self.speed = 10
        self.control = Control() # TODO: сделать управление

    def tick(self):
        self.camera.tick()

    def on_button_press(self, button):
        action = self.control.get_action(button)


class Control: # управление игроком

    def __init__(self):
        # управление
        self.buttons = dict()

    def get_action(self, button):
        return self.buttons[button]

    def bind_action(self, button, action):
        self.buttons[button] = action


class Action:

    def perform(self, player, button):
        pass


class MoveAction(Action):

    def __init__(self, direction): # direction - кортеж с направлениями по x и y - числами от 0 до 1
        self.direction = direction

    def perform(self, player, button):
        player.move(self.direction[0] * player.speed, self.direction[1] * player.speed)
