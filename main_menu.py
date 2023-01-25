import random

import pygame

import main
from game_objects import GameObject, FadingText
from world import World


class MainMenu(World):

    def __init__(self):
        super().__init__()


class Button(GameObject):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image, priority=1)

    def click(self, pos):
        # тут просто для наглядности вывод текста сделал, в наследниках это надо переопределять
        fading_text = FadingText(pos[0] - 30, pos[1] - 20, self.world, 'click!', (0, 255, 0))
        self.world.add_object(fading_text)
        self.rect.x = random.randint(100, 1000)
        self.rect.y = random.randint(60, 600)


class StartButton(Button):

    def __init__(self, x, y, world, image, game_state):
        super().__init__(x, y, world, image)
        self.game_state = game_state

    def click(self, pos):
        print("click!")
        self.game_state.start = True


def load_menu(game_state) -> MainMenu:
    pattern = ['----------------',
               '----------------',
               '----------------',
               '--------S-------',
               '----------------',
               '----------------',
               '----------------',
               '----------------',
               '----------------']  # 16x9
    # S - кнопка "новая игра"
    # L - кнопка "загрузить игру" WIP
    # O - кнопка "настройки" WIP
    # E - кнопка "выйти из игры" WIP
    new_game = pygame.image.load('assets/main_menu/new_game.png')
    screen_size = (game_state.game.width, game_state.game.height)
    background = pygame.transform.scale(pygame.image.load('assets/main_menu/background.jpg'),
                                        screen_size)
    menu = MainMenu()
    menu.add_object(GameObject(0, 0, menu, background))
    for y in range(len(pattern)):
        row = pattern[y]
        for x in range(len(row)):
            c = row[x]
            if c == "S":
                button = StartButton(100, 100, menu, new_game, game_state)
                button.rect.center = screen_size[0] / len(row) * x, screen_size[1] / len(pattern) * y
                menu.add_object(button)
    return menu
