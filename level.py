import json
import random

import menu
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

    def set_player(self, player):
        super().set_player(player)
        player.rect.x = self.start_pos[0]
        player.rect.y = self.start_pos[1]

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
            # из-за того что весь мир двигается камерой надо сохранять тайлы
            # думаю переделать камеру и сделать сохранение только обьектов
            # тайлы бы загружались там где они настроены
            data = {'tiles': dict(),
                    'objects': dict()}
            for tile in self.tiles.values():
                if not tile.is_saveable():
                    continue
                save = tile.save()
                data['tiles'][str(tile.id)] = save
            for obj in self.game_objects.values():
                if not obj.is_saveable():
                    continue
                save = obj.save()
                data['objects'][str(obj.id)] = save
            json.dump(data, save_file)


def load_level():
    with open('assets/level1/options.json') as options_file:
        options = json.load(options_file)
    with open('assets/level1/objects.json') as objects_file:
        objects_data = json.load(objects_file)
    with open('assets/level1/layout.txt') as map_file:
        layout = list(map(lambda s: s.replace('\n', ''), map_file.readlines()))
    w = Level('level1')
    menu.fill_world(w, layout, objects_data, options)
    return w
