import pygame

import main
from menu import load_world, Button, ExitButton
from world import World, Background


class MainMenuButton(Button):

    def __init__(self, x, y, world, image, game_state):
        super().__init__(x, y, world, image)
        self.game_state = game_state

    def click(self, pos):
        self.game_state.next_state = lambda game, prev_state: main.MainMenuState(game)


def load_menu(game_state) -> World:
    pattern = ['----------------',
               '----------------',
               '----------------',
               '--------M-------',
               '----------------',
               '----------------',
               '----------------',
               '--------E-------',
               '----------------']  # 16x9, можно любое разрешение
    # M - кнопка 'вернуться в главное меню'
    new_game = pygame.image.load('assets/main_menu/new_game.png')
    exit_icon = pygame.image.load("assets/main_menu/exit.png")
    screen_size = (game_state.game.width, game_state.game.height)
    menu = load_world(screen_size,
                      pattern,
                      {'M': lambda x, y, w: MainMenuButton(x, y, w, new_game, game_state),
                       'E': lambda x, y, w: ExitButton(x, y, w, exit_icon, game_state.game)})
    background = pygame.Surface(screen_size)
    background.set_alpha(125)
    menu.background = Background(background)
    return menu
