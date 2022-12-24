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
            self.mode.tick(self)


class Renderer:
    # можно всякие шейдеры добавить

    def render(self, world, screen, camera):
        screen.fill((0, 0, 0))
        rect = pygame.Rect(10, 10, 10, 10)
        pygame.draw.rect(screen, pygame.Color('white'), rect, 1)
        world.sprites_group.draw(screen)
        #for obj in world.game_objects:
        #    obj.render(camera, screen)
