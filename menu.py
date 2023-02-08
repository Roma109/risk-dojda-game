import random

import main
from game_objects import GameObject, FadingText
from world import World


class Button(GameObject):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image, None, priority=1)

    def click(self, pos):
        # тут просто для наглядности вывод текста сделал, в наследниках это надо переопределять
        fading_text = FadingText(pos[0] - 30, pos[1] - 20, self.world, 'click!', (0, 255, 0))
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
