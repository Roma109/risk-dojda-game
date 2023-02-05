import pygame.display


class ObjectFollowMode:

    def __init__(self, obj):
        self.obj = obj

    def tick(self, camera):
        if self.obj.active:
            camera.x = self.obj.rect.centerx - camera.width // 2
            camera.y = self.obj.rect.centery - camera.height // 2


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        display_info = pygame.display.Info()
        self.width = display_info.current_w
        self.height = display_info.current_h
        self.x = 0
        self.y = 0
        self.mode = None

    def set_mode(self, mode):
        self.mode = mode

    def tick(self):
        if self.mode is not None:
            self.mode.tick(self)
