import pygame

import game_over
import level
import main_menu
import menu
import options
import pause
from camera import ObjectFollowMode
from player import Player


class Game:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.state = None
        self.screen = None
        self.display_info = None
        self.running = False
        self.clock = pygame.time.Clock()
        self.fps = 30

    def start(self):
        if self.running:
            raise RuntimeError('Game already started!')
        pygame.init()
        pygame.display.set_caption("Опасность дождя")
        self.display_info = pygame.display.Info()
        self.width = self.display_info.current_w
        self.height = self.display_info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.state = MainMenuState(self)
        while self.running:
            self.update()
            self.clock.tick(self.fps)

    def update(self):
        self.state = self.state.update()
        if not self.running:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.state.on_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.state.button_press(event.key)
            elif event.type == pygame.KEYUP:
                self.state.button_release(event.key)

    def close(self):
        self.running = False
        pygame.display.quit()
        pygame.quit()


class GameState:

    def __init__(self, game, world=None):
        self.game = game
        self.world = world
        self.next_state = None

    def update(self):
        if self.next_state:
            return self.next_state(self.game, self)
        return self

    def on_click(self, screen_pos):
        pass

    def button_press(self, button):
        pass

    def button_release(self, button):
        pass


class MainMenuState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.world = main_menu.load_menu(self)

    def update(self):
        self.game.screen.fill((0, 0, 0))
        self.world.update()
        self.world.render(self.game.screen)
        pygame.display.flip()
        return super().update()

    def on_click(self, pos):
        clicked_obj = self.world.get_obj(pos)
        if clicked_obj is None or not isinstance(clicked_obj, menu.Button):
            return
        clicked_obj.click(pos)


class OptionsState(GameState):

    def __init__(self, game, prev_state):
        super().__init__(game)
        self.world = options.load_menu(self)
        self.prev_state = prev_state

    def update(self):
        self.game.screen.fill((0, 0, 0))
        self.world.update()
        self.world.draw(self.game.screen)
        pygame.display.flip()
        return super().update()

    def on_click(self, pos):
        clicked_obj = self.world.get_obj(pos)
        if clicked_obj is None or not isinstance(clicked_obj, menu.Button):
            return
        clicked_obj.click(pos)


class GameInProgressState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.world = level.load_level()
        self.player = Player(0, 0,
                             self.world, pygame.image.load('assets/player.jpg'))
        self.world.add_human(self.player)
        self.world.camera.set_mode(ObjectFollowMode(self.player))
        print('game in progress!')

    def update(self):
        self.game.screen.fill((0, 0, 0))
        self.world.update()
        self.world.render(self.game.screen)
        pygame.display.flip()
        if not self.player.active:
            self.next_state = lambda game, prev_state: GameOverState(game, prev_state.world)
        return super().update()

    def button_press(self, button):
        if button == pygame.K_ESCAPE:
            self.next_state = lambda game, prev_state: GamePauseState(game, prev_state)
        for key in self.player.control.buttons:
            if key == button:
                self.player.control.get_action(key).start(self.player)

    def button_release(self, button):
        for key in self.player.control.buttons:
            if key == button:
                self.player.control.get_action(key).end(self.player)


class GamePauseState(GameState):

    def __init__(self, game, prev_state):
        super().__init__(game)
        self.prev_state = prev_state
        self.world = pause.load_menu(self)

    def update(self):
        self.game.screen.fill((0, 0, 0))
        self.world.update()
        self.prev_state.world.render(self.game.screen)
        self.world.render(self.game.screen)
        pygame.display.flip()
        return super().update()

    def on_click(self, pos):
        clicked_obj = self.world.get_obj(pos)
        if clicked_obj is None or not isinstance(clicked_obj, menu.Button):
            return
        clicked_obj.click(pos)


class GameOverState(GameState):

    def __init__(self, game, world):
        super().__init__(game)
        self.background_world = world
        self.world = game_over.load_menu(self)

    def update(self):
        self.game.screen.fill((0, 0, 0))
        self.world.update()
        self.background_world.render(self.game.screen)
        self.world.render(self.game.screen)
        pygame.display.flip()
        return super().update()

    def on_click(self, pos):
        clicked_obj = self.world.get_obj(pos)
        if clicked_obj is None or not isinstance(clicked_obj, menu.Button):
            return
        clicked_obj.click(pos)


GAME = Game()


def main():
    global GAME
    GAME.start()


def get_game():
    return GAME


if __name__ == '__main__':
    main()
