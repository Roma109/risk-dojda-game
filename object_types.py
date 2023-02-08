import pygame.image

import enemies
import world
import player

ENEMY = 0
BOSS = 1
TILE = 2
SPAWNER = 11
OTHER = 1000


# Для игровых обьектов, которые надо сохранять/загружать есть типы
# Эти типы принимают сохранённые данные об обьекте и возвращают загруженный обьект
# хотел через пиклз сделать, но спрайты отказываются сохраняться
class ObjectType:

    def __init__(self, key, data, type):
        self.key = key
        self.data = data
        self.type = type

    def load(self, data, w):
        pass

    def create(self, x, y, w):
        pass


class TileType(ObjectType):

    def __init__(self, key, data):
        super().__init__(key, data, TILE)
        self.image = pygame.image.load(data["image"])
        self.collideable = data["collideable"]
        self.spawner = data["spawner"]

    def load(self, data, w):
        x, y = data['x'], data['y']
        tile = self.create(0, 0, w)
        tile.rect.x = x
        tile.rect.y = y
        return tile
        # из-за кривой костыльной камеры приходится так загружать тайлы

    def create(self, x, y, w):
        if self.collideable:
            if self.spawner:
                return enemies.SpawnerTile(x, y, w, self.image, self.key)
            return world.CollideableTile(x, y, w, self.image, self.key)
        else:
            return world.Tile(x, y, w, self.image, self.key)


class PlatformType(ObjectType):

    def __init__(self, key, data):
        super().__init__(key, data, OTHER)
        self.image = pygame.image.load(data["image"])

    def load(self, data, w):
        x, y = data['x'], data['y']
        return self.create(x, y, w)

    def create(self, x, y, w):
        return world.Platform(x, y, w, self.image, self.key)


class SpawnerType(ObjectType):

    def __init__(self, key, data):
        super().__init__(key, data, SPAWNER)
        self.image = pygame.image.load(data["image"])

    def load(self, data, w):
        x, y = data['x'], data['y']
        return self.create(x, y, w)

    def create(self, x, y, w):
        return enemies.SpawnerTile(x, y, w, self.image, self.key)


class GoalType(ObjectType):
    def __init__(self, key, data):
        super().__init__(key, data, TILE)
        self.image = pygame.image.load(data["image"])
        self.collideable = data["collideable"]

    def load(self, data, w):
        x, y = data['x'], data['y']
        tile = self.create(0, 0, w)
        tile.rect.x = x
        tile.rect.y = y
        return tile

    def create(self, x, y, w):
        w.add_object(player.Item(x, y, w, 'goal'))
        return world.Tile(x, y, w, self.image, self.key),


class EnemyType(ObjectType):

    def __init__(self, key, data):
        super().__init__(key, data, ENEMY)
        self.image = pygame.image.load(data['image'])
        self.maxhp = data["maxhp"]
        self.damage = data["damage"]

    def load(self, data, w):
        x, y = data['x'], data['y']
        wisp = self.create(x, y, w)
        wisp.apply(data)
        return wisp

    def create(self, x, y, w):
        wisp = enemies.Enemy(x, y, w, self.image, self.key, self.maxhp)
        for key, value in self.data.items():
            if key in ['image', 'maxhp', 'damage', 'provider']:
                continue
            setattr(wisp, key, value)
        return wisp


class BossType(ObjectType):

    def __init__(self, key, data):
        super().__init__(key, data, BOSS)
        self.image = pygame.image.load(data['image'])
        self.maxhp = data["maxhp"]
        self.damage = data["damage"]

    def load(self, data, w):
        x, y = data['x'], data['y']
        wisp = self.create(x, y, w)
        wisp.apply(data)
        return wisp

    def create(self, x, y, w):
        boss = enemies.BossEnemy(x, y, w, self.image, self.key, self.maxhp)
        for key, value in self.data.items():
            if key in ['image', 'maxhp', 'damage', 'provider']:
                continue
            setattr(boss, key, value)
        return boss


# планировал сделать сохранение дефолтных значений в конструкторе
# надо проверить надобность и на словарь заменить если чё
class ObjectTypes:

    def __init__(self):
        self.types = dict()

    def register(self, type):
        self.types[type.key] = type

    def get(self, key):
        return self.types.get(key, None)

    def get_by_type(self, type):
        valid = list()
        for obj_type in self.types.values():
            if obj_type.type == type:
                valid.append(obj_type)
        return valid
