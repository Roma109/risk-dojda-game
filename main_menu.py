import pygame

from game_objects import GameObject
from world import World


class MainMenu(World):

    def __init__(self):
        super().__init__()


class Button(GameObject):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)

    def click(self, pos):
        print('click!')


def load_menu() -> MainMenu:
    new_game = pygame.image.load('assets/main_menu/new_game.png')
    menu = MainMenu()
    menu.add_object(Button(10, 10, menu, new_game))
    return menu
