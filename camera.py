import main


class ObjectFollowMode:

    def __init__(self, obj):
        self.obj = obj

    def tick(self, camera):
        camera.update(self.obj)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.mode = None

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        display_info = main.get_game().display_info
        self.dx = -(target.rect.x + target.rect.w // 2 - display_info.current_w // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - display_info.current_h // 2)

    def set_mode(self, mode):
        self.mode = mode

    def tick(self):
        if self.mode is not None:
            self.mode.update(self)
