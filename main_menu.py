import pygame

import main
from menu import load_world, Button, ExitButton, OptionsButton
from world import World, Background


class StartButton(Button):

    def __init__(self, x, y, world, image, game_state):
        super().__init__(x, y, world, image)
        self.game_state = game_state

    def click(self, pos):
        self.game_state.game.state = main.GameInProgressState(self.game_state.game)


def load_menu(game_state) -> World:
    pattern = ['----------------',
               '----------------',
               '----------------',
               '--------S-------',
               '----------------',
               '--------O-------',
               '----------------',
               '--------E-------',
               '----------------']  # 16x9, можно любое разрешение
    # S - кнопка "новая игра"
    # L - кнопка "загрузить игру" WIP
    # O - кнопка "настройки"
    # E - кнопка "выйти из игры"
    new_game = pygame.image.load('assets/main_menu/New game Button.png')
    options_icon = pygame.image.load('assets/main_menu/Options Button.png')
    exit_icon = pygame.image.load("assets/main_menu/Exit Button.png")
    screen_size = (game_state.game.width, game_state.game.height)
    menu = load_world(screen_size,
                      pattern,
                      {'S': lambda x, y, w: StartButton(x, y, w, new_game, game_state),
                       'O': lambda x, y, w: OptionsButton(x, y, w, options_icon, game_state),
                       'E': lambda x, y, w: ExitButton(x, y, w, exit_icon, game_state.game)})
    background = pygame.transform.scale(pygame.image.load('assets/main_menu/background.jpg'),
                                        screen_size)
    menu.background = Background(background)
    return menu
