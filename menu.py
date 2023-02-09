import json
import random

import pygame.image

import level
import main
import object_types
import world
from game_objects import GameObject, FadingText
from world import World


class Button(GameObject):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image, None, priority=1)

    def click(self, pos):
        # тут просто для наглядности вывод текста сделал, в наследниках это надо переопределять
        fading_text = FadingText(pos[0] - 30, pos[1] - 20, self.world, 'ура!', (0, 255, 0))
        self.world.add_object(fading_text)
        self.rect.x = random.randint(100, 1000)
        self.rect.y = random.randint(60, 600)


class ExitButton(Button):

    def __init__(self, x, y, world, image, game):
        super().__init__(x, y, world, image)
        self.game = game

    def click(self, pos):
        self.game.close()


class OptionsButton(Button):

    def __init__(self, x, y, world, image, game_state):
        super().__init__(x, y, world, image)
        self.game_state = game_state

    def click(self, pos):
        self.game_state.game.state = main.OptionsState(self.game_state.game, self.game_state)


class MainMenuButton(Button):

    def __init__(self, x, y, world, image, game_state):
        super().__init__(x, y, world, image)
        self.game_state = game_state

    def click(self, pos):
        self.game_state.game.state = main.MainMenuState(self.game_state.game)


def create_world(name, screen_size, pattern, elements) -> World:
    w = World(name)
    for y in range(len(pattern)):
        row = pattern[y]
        for x in range(len(row)):
            c = row[x]
            if c in elements:
                obj = elements[c](0, 0, w)
                obj.rect.center = screen_size[0] / len(row) * x, screen_size[1] / len(pattern) * y
                w.add_object(obj)
    return w


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


def fill_world(w, layout, objects_data, options, cached_types=None):
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
            # нужно чтобы гарантировать что все тайлы выстроены в сеточку
            if not isinstance(type, object_types.TileType):
                obj_x *= world.TILE_SIZE
                obj_y *= world.TILE_SIZE
            w.add(type.create(obj_x, obj_y, w))
    background = options['background']
    if background:
        w.background = world.Background(pygame.image.load(background))


# Чтобы загрузить мир нужно чтобы существовал файл "название мира.json"
# И в папке "assets/название мира" существовали файлы "objects.json", "options.json"
# Пока что загружаются только level.Level
# Посчитал ненужным загружать обычные миры
def load_level(name):
    with open('assets/level1/options.json') as options_file:
        options = json.load(options_file)
    with open('assets/level1/objects.json') as objects_file:
        objects_data = json.load(objects_file)
    with open('assets/level1/layout.txt') as layout_file:
        layout = list(map(lambda s: s.replace('\n', ''), layout_file.readlines()))
    with open(f'{name}.json') as save_file:
        save_data = json.load(save_file)
    w = level.Level(name)
    cached_types = load_types(objects_data)
    fill_world(w, layout, objects_data, options, cached_types)
    for id, data in save_data['objects'].items():
        data['id'] = id
        w.add_object(cached_types[data['key']].load(data, w))
    return w


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
