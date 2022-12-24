import pygame


class PlayerFollowMode:

    def __init__(self, player):
        self.player = player

    def tick(self, camera):
        camera.x = self.player.x
        camera.y = self.player.y


class Camera:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.mode = None

    def set_mode(self, mode):
        self.mode = mode

    def tick(self):
        if self.mode is not None:
            self.mode.update(self)
