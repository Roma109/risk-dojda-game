import pygame

import main
from menu import create_world, Button, ExitButton, OptionsButton, MainMenuButton
from world import World, Background

class ContinueButton(Button):

    def __init__(self, x, y, world, image, game_state):
        super().__init__(x, y, world, image)
        self.game_state = game_state

    def click(self, pos):
        self.game_state.game.state = self.game_state.prev_state


class SaveExitButton(Button):

    def __init__(self, x, y, world, image, game_state):
        super().__init__(x, y, world, image)
        self.game_state = game_state

    def click(self, pos):
        self.game_state.prev_state.world.save()
        self.game_state.game.state = main.MainMenuState(self.game_state.game)


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
    # O - кнопка "настройки"
    # E - кнопка "сохранить и выйти" WIP
    new_game = pygame.image.load('assets/main_menu/Resume Button.png')
    options_icon = pygame.image.load('assets/main_menu/Options Button.png')
    exit_icon = pygame.image.load("assets/main_menu/Exit Button.png")
    return_to_menu = pygame.image.load('assets/main_menu/Menu Button.png')
    screen_size = (game_state.game.width, game_state.game.height)
    menu = create_world('pause',
                        screen_size,
                        pattern,
                        {'C': lambda x, y, w: ContinueButton(x, y, w, new_game, game_state),
                         'O': lambda x, y, w: OptionsButton(x, y, w, options_icon, game_state),
                         'E': lambda x, y, w: SaveExitButton(x, y, w, exit_icon, game_state),
                         'M': lambda x, y, w: MainMenuButton(x, y, w, return_to_menu, game_state)})
    background = pygame.Surface(screen_size)
    background.set_alpha(125)
    menu.background = Background(background)
    return menu
