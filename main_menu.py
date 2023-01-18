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
        # screen_pos - положение курсора на экране, game_pos - положение курсора в игровом мире
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

    new_game = pygame.image.load('assets/main_menu/new_game.png')
    #TODO: получить размеры экрана 
    background = pygame.transform.scale(pygame.image.load('assets/main_menu/background.jpg'),
                                        (game_state.game.width, game_state.game.height))
    # TODO: начать игру по нажатию на кнопку
    menu = MainMenu()
    menu.add_object(StartButton(10, 10, menu, new_game, game_state))
    return menu
