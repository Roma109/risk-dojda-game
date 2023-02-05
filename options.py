import pygame

from menu import load_world, Button
from world import World, Background


class BackButton(Button):

    def __init__(self, x, y, world, image, game_state):
        super().__init__(x, y, world, image)
        self.game_state = game_state

    def click(self, pos):
        self.game_state.prev_state.next_state = None
        self.game_state.game.state = self.game_state.prev_state


def load_menu(game_state) -> World:
    pattern = ['----------------',
               '----------------',
               '----------------',
               '----------------',
               '----------------',
               '----------------',
               '----------------',
               '-------------B--',
               '----------------']  # 16x9, можно любое разрешение
    # B - кнопка 'назад'
    back = pygame.image.load('assets/main_menu/Back Button.png')
    screen_size = (game_state.game.width, game_state.game.height)
    menu = load_world(screen_size,
                      pattern,
                      {'B': lambda x, y, w: BackButton(x, y, w, back, game_state)})
    background = pygame.Surface(screen_size)
    background.set_alpha(125)
    menu.background = Background(background)
    return menu
