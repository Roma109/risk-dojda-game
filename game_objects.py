import uuid

import pygame.sprite


class GameObject(pygame.sprite.Sprite):

    def __init__(self, x, y, world, image, priority=-1, active=True):
        super().__init__(world)
        self.world = world
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.priority = priority
        self.active = active
        self.id = uuid.uuid4()

    def update(self):
        pass

    def collide(self, obj):
        pass

    def is_inside(self, point):
        return self.rect.collidepoint(point[0], point[1])

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def collide(self, other):
        pass


class Platform(GameObject):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)

    def collide(self, entity):
        if entity.rect.collidepoint(self.rect.midtop) or \
           entity.rect.collidepoint(self.rect.topright) or \
           entity.rect.collidepoint(self.rect.topleft):
            if entity.vy > 0:
                entity.vy = 0
                entity.on_ground = True


class Entity(GameObject):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image, priority=0)
        self.vx = 0
        self.vy = 0
        self.on_ground = False

    def update(self):
        if not self.on_ground:
            self.vy += 9.8 / 30
        self.move(self.vx, self.vy)
        self.vx *= 0.7
        if abs(self.vx) <= 0.005:
            self.vx = 0
        if abs(self.vy) <= 0.005:
            self.vy = 0
        self.on_ground = False


class Creature(Entity):

    def __init__(self, x, y, world, image, hp, maxhp):
        super().__init__(x, y, world, image)
        self.hp = hp
        self.maxhp = maxhp

    def damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.kill()

    def kill(self):
        self.world.remove_object(self)


class FadingText(GameObject):

    def __init__(self, x, y, world, text, color=(255, 255, 255), alpha=255, font=None):
        if font is None:
            font = pygame.font.SysFont('Comic Sans MS', 30)
        self.font = font
        self.text = text
        self.color = color
        self.alpha = alpha
        super().__init__(x, y, world, self.font.render(text, False, color))
        self.image.set_alpha(self.alpha)

    def update(self):
        self.alpha -= 5
        if self.alpha <= 0:
            self.active = False
            self.world.remove_object(self)
            return
        self.image = self.font.render(self.text, False, self.color)
        self.image.set_alpha(self.alpha)
