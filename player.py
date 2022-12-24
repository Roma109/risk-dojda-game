from game_objects import Creature
from renderer import Camera, PlayerFollowMode


class Human(Creature):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)


class Player(Human):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)
        self.camera = Camera()
        self.camera.mode = PlayerFollowMode(self)

    def tick(self):
        self.camera.tick()