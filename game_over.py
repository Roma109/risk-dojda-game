import pygame

import main
from menu import create_world, ExitButton, MainMenuButton, Button
from world import World, Background


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
    new_game = pygame.image.load('assets/main_menu/Menu Button.png')
    exit_icon = pygame.image.load("assets/main_menu/Exit Button.png")
    screen_size = (game_state.game.width, game_state.game.height)
    menu = create_world('game_over',
                        screen_size,
                        pattern,
                        {'M': lambda x, y, w: MainMenuButton(x, y, w, new_game, game_state),
                         'E': lambda x, y, w: ExitButton(x, y, w, exit_icon, game_state.game)})
    background = pygame.Surface(screen_size)
    background.set_alpha(125)
    menu.background = Background(background)
    return menu


def load_score(game_state) -> World:
    pattern = ['----------------',
               '--------W-------',
               '----------------',
               '----------------',
               '--------M-------',
               '----------------',
               '----------------',
               '--------E-------',
               '----------------']  # 16x9, можно любое разрешение
    # M - кнопка 'вернуться в главное меню'
    new_game = pygame.image.load('assets/main_menu/Menu Button.png')
    exit_icon = pygame.image.load("assets/main_menu/Exit Button.png")
    game_won = pygame.image.load("assets/main_menu/win.png").convert_alpha()
    screen_size = (game_state.game.width, game_state.game.height)
    menu = create_world('game_over',
                        screen_size,
                        pattern,
                        {'M': lambda x, y, w: MainMenuButton(x, y, w, new_game, game_state),
                         'E': lambda x, y, w: ExitButton(x, y, w, exit_icon, game_state.game),
                         'W': lambda x, y, w: Button(x, y, w, game_won)})
    background = pygame.Surface(screen_size)
    background.set_alpha(125)
    menu.background = Background(background)
    print('win')
    return menu