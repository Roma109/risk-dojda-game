from game_objects import Creature
from renderer import Camera, PlayerFollowMode


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
        self.camera.mode = PlayerFollowMode(self)
        self.speed = 10
        self.control = Control()

    def tick(self):
        self.camera.tick()

    def on_button_press(self, button):
        action = self.control.get_action(button)


class Control: # управление игроком

    def __init__(self):
        self.buttons = dict()

    def get_action(self, button):
        return self.buttons[button]

    def bind_action(self, button, action):
        self.buttons[button] = action


class Action:

    def perform(self, player, button):
        pass


class MoveAction(Action):

    def __init__(self, direction):
        self.direction = direction

    def perform(self, player, button):
        player.move(self.direction[0] * player.speed, self.direction[1] * player.speed)