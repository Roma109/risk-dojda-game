import pygame.display


class ObjectFollowMode:

    def __init__(self, obj):
        self.obj = obj

    def tick(self, camera):
        if self.obj.active:
            camera.update(self.obj)
        else:
            camera.dx = 0
            camera.dy = 0


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, screen_width=-1, screen_height=-1):
        if screen_width == -1 or screen_height == -1:
            display_info = pygame.display.Info()
            screen_width = display_info.current_w
            screen_height = display_info.current_h
        self.dx = 0
        self.dy = 0
        self.w = screen_width
        self.h = screen_height
        self.mode = None

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.w // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.h // 2)

    def set_mode(self, mode):
        self.mode = mode

    def tick(self):
        if self.mode is not None:
            self.mode.tick(self)
