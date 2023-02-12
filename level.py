import json
import random

import pygame

import object_types
import player
import world


class Level(world.World):

    def __init__(self, name, start_pos=(0, 0), max_enemies=10, spawn_delay=90):
        super().__init__(name)
        self.max_enemies = max_enemies
        self.start_pos = start_pos
        self.spawn_delay = spawn_delay
        self.spawn_time = 0
        self.enemies = []

    def update(self):
        if len(self.enemies) < self.max_enemies:
            self.spawn_time += 1
            if self.spawn_time >= self.spawn_delay:
                self.spawn_time = 0
                enemy_types = self.types.get_by_type(object_types.ENEMY)
                if enemy_types:
                    enemy = random.choice(enemy_types).create(0, 64, self)
                    self.add_object(enemy)
                    self.enemies.append(enemy)
        super().update()
        for enemy in list(self.enemies):
            if not enemy.active:
                self.enemies.remove(enemy)

    def save(self):
        with open(f"{self.name}.json", "w") as save_file:
            data = {'objects': dict()}
            for obj in self.game_objects.values():
                if not obj.is_saveable():
                    continue
                save = obj.save()
                data['objects'][str(obj.id)] = save
            data['player'] = self.player.save()
            json.dump(data, save_file)


def load_types(objects_data):
    tiles = objects_data['tiles']
    objects = objects_data['objects']
    cached_types = dict()
    for key in tiles.keys():
        type = object_types.TileType(key, tiles[key])
        cached_types[key] = type
    for key in objects.keys():
        obj_data = objects[key]
        type = get_class(obj_data['provider'])(key, obj_data)
        cached_types[key] = type
    return cached_types


def fill_world(w, layout, objects_data, options, cached_types=None, loading_save=False):
    if cached_types is None:
        cached_types = load_types(objects_data)
    for type in cached_types.values():
        w.register_type(type)
    layout_instructions = options["layout"]
    for y in range(len(layout)):
        row = layout[y]
        for x in range(len(row)):
            elem = row[x]
            if elem not in layout_instructions:
                raise ValueError('Unknown layout elem: ' + elem)
            obj_key = layout_instructions[elem]
            obj_x = x
            obj_y = y
            type = cached_types[obj_key]
            if loading_save and elem == 'S':
                print('story_detected --> continuing without adding...')
                continue
            # нужно чтобы гарантировать что все тайлы выстроены в сеточку
            if not isinstance(type, object_types.TileType):
                obj_x *= world.TILE_SIZE
                obj_y *= world.TILE_SIZE
            w.add(type.create(obj_x, obj_y, w))
    background = options['background']
    if background:
        w.background = world.Background(pygame.image.load(background))


# Чтобы загрузить мир нужно чтобы существовал файл "название мира.json"
# И в папке "assets/название мира" существовали файлы "object_types.json", "options.json"
# Пока что загружаются только level.Level
# Посчитал ненужным загружать обычные миры
def load_level(name):
    with open(f'assets/{name}/options.json') as options_file:
        options = json.load(options_file)
    with open(f'assets/{name}/object_types.json') as objects_file:
        objects_data = json.load(objects_file)
    with open(f'assets/{name}/layout.txt') as layout_file:
        layout = list(map(lambda s: s.replace('\n', ''), layout_file.readlines()))
    with open(f'{name}.json') as save_file:
        save_data = json.load(save_file)
    w = Level(name)
    w.start_pos = options['spawnpoint']['x'], options['spawnpoint']['y']
    cached_types = load_types(objects_data)
    fill_world(w, layout, objects_data, options, cached_types, loading_save=True)
    for id, data in save_data['objects'].items():
        print(id, '  #####  ', data )
        if data['key'] == 'rocket':
            continue
        data['id'] = id
        w.add_object(cached_types[data['key']].load(data, w))
    return w


def load_player(name, w):
    with open(f'{name}.json') as save_file:
        save_data = json.load(save_file)['player']
    p = player.Player(save_data['x'], save_data['y'], w, pygame.image.load('assets/player.png'))
    p.apply(save_data)
    return p


# получает класс по названию, используется для загрузки типа обьекта
# скопировано из интернета
def get_class(name):
    # Reflection: try to get the exception class

    # Try to split the name on dots,
    # in case it contains a module path
    parts = name.split('.')

    if len(parts) == 1:
        # If it didn't have a module path,
        # try loading the class from built-ins
        try:
            m = __import__('builtins')
        except ImportError:
            m = __import__('__builtin__')

        m = getattr(m, parts[0])

    else:
        # If it did have a module path,
        # load the module and then get the class
        module = ".".join(parts[:-1])
        m = __import__(module)

        for comp in parts[1:]:
            m = getattr(m, comp)

    return m


def create_level():
    with open('assets/level1/options.json') as options_file:
        options = json.load(options_file)
    with open('assets/level1/object_types.json') as objects_file:
        objects_data = json.load(objects_file)
    with open('assets/level1/layout.txt') as map_file:
        layout = list(map(lambda s: s.replace('\n', ''), map_file.readlines()))
    with open('assets/level1/objects.json') as objects_file:
        objects = json.load(objects_file)
    w = Level('level1')
    w.start_pos = options['spawnpoint']['x'], options['spawnpoint']['y']
    fill_world(w, layout, objects_data, options)
    for obj in objects['objects']:
        provider = w.types.get(obj['type'])
        x, y = obj['x'], obj['y']
        w.add(provider.create(x, y, w))
    return w
