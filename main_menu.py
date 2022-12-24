import pygame

from game_objects import GameObject, FadingText
from world import World


class MainMenu(World):

    def __init__(self):
        super().__init__()


class Button(GameObject):

    def __init__(self, x, y, world, image):
        super().__init__(x, y, world, image)

    def click(self, screen_pos, game_pos):
        # screen_pos - положение курсора на экране, game_pos - положение курсора в игровом мире
        # тут просто для наглядности вывод текста сделал, в наследниках это надо переопределять
        fading_text = FadingText(screen_pos[0] - 30, screen_pos[1] - 20, self.world, 'click!', (0, 255, 0))
        self.world.add_object(fading_text)


def load_menu() -> MainMenu:
    new_game = pygame.image.load('assets/main_menu/new_game.png')
    # TODO: начать игру по нажатию на кнопку
    menu = MainMenu()
    menu.add_object(Button(10, 10, menu, new_game))
    return menu
