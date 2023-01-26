import pygame

from menu import load_world, Button, ExitButton, OptionsButton
from world import World, Background


class ContinueButton(Button):

    def __init__(self, x, y, world, image, game_state):
        super().__init__(x, y, world, image)
        self.game_state = game_state

    def click(self, pos):
        self.game_state.game.state = self.game_state.prev_state


def load_menu(game_state) -> World:
    pattern = ['----------------',
               '----------------',
               '--------C-------',
               '----------------',
               '--------O-------',
               '----------------',
               '--------E-------',
               '----------------',
               '----------------']  # 16x9, можно любое разрешение
    # C - кнопка "продолжить"
    # E - кнопка "сохранить и выйти" WIP
    new_game = pygame.image.load('assets/main_menu/new_game.png')
    options_icon = pygame.image.load('assets/main_menu/options.png')
    exit_icon = pygame.image.load("assets/main_menu/exit.png")
    screen_size = (game_state.game.width, game_state.game.height)
    menu = load_world(screen_size,
                      pattern,
                      {'C': lambda x, y, w: ContinueButton(x, y, w, new_game, game_state),
                       'O': lambda x, y, w: OptionsButton(x, y, w, options_icon, game_state),
                       'E': lambda x, y, w: ExitButton(x, y, w, exit_icon, game_state.game)})
    background = pygame.Surface(screen_size)
    background.set_alpha(125)
    menu.background = Background(background)
    return menu
