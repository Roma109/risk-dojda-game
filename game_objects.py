import uuid

import pygame.sprite


class Collideable:

    def collide(self, other):
        pass

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
        self.vx = 0
        self.vy = 0

    def update(self):
        pass

    def is_inside(self, point):
        return self.rect.collidepoint(point[0], point[1])

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def get_pos(self):
        return self.rect.x, self.rect.y


class Entity(GameObject, Collideable):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image, priority=0)
        self.vx = 0
        self.vy = 0
        self.on_ground = 0

    def update(self):
        if not self.active:
            return
        if not self.on_ground:
            self.vy += 0.3266667  # 9.8 / 30
        self.move(self.vx, self.vy)
        self.vx *= 0.7
        if abs(self.vx) <= 0.005:
            self.vx = 0
        if abs(self.vy) <= 0.005:
            self.vy = 0
        if self.on_ground:
            self.on_ground -= 1


class Creature(Entity):

    def __init__(self, x, y, world, image, hp, maxhp):
        super().__init__(x, y, world, image)
        self.hp = hp
        self.maxhp = maxhp
        self.direction = (0, 0)
        self.speed = 10
        self.jump_power = 10
        self.invisibility_frames = 0

    def damage(self, amount):
        if self.invisibility_frames:
            return
        self.invisibility_frames = 30
        self.hp = max(0, self.hp - amount)
        self.world.add_object(FadingText(self.rect.x, self.rect.y, self.world, str(amount), (255, 100, 100), 200))
        if self.hp == 0:
            self.kill()

    def kill(self):
        self.vx = 0
        self.vy = 0
        self.direction = (0, 0)
        self.active = False
        self.world.remove_object(self)

    def update(self):
        if not self.active:
            return
        dx, dy = self.direction
        if dx != 0:
            self.vx = dx * self.speed
        if dy != 0 and self.on_ground:
            self.vy = dy * self.jump_power
        if self.invisibility_frames:
            self.invisibility_frames -= 1
        super().update()


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
