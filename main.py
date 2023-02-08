import sys

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

    def load(self):
        name = 'level1'
        w = level.load_level(name)
        p = level.load_player(name, w)
        self.state = GameInProgressState(self, w, p)

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
        sys.exit(0)


class GameState:

    def __init__(self, game, world=None):
        self.game = game
        self.world = world

    def update(self):
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
        return self

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
        return self

    def on_click(self, pos):
        clicked_obj = self.world.get_obj(pos)
        if clicked_obj is None or not isinstance(clicked_obj, menu.Button):
            return
        clicked_obj.click(pos)


class GameInProgressState(GameState):

    def __init__(self, game, w=None, player=None):
        super().__init__(game)
        if w is None:
            w = level.create_level()
        if player is None:
            player = Player(w.start_pos[0], w.start_pos[1],
                            w, pygame.image.load('assets/player.png'))
        self.world = w
        self.player = player
        self.world.set_player(self.player)
        self.world.camera.set_mode(ObjectFollowMode(self.player))
        print('game in progress!')
        print(self.world.game_objects)

    def update(self):
        self.game.screen.fill((0, 0, 0))
        self.world.update()
        self.world.render(self.game.screen)
        pygame.display.flip()
        if not self.player.active:
            return GameOverState(self.game, self.world)
        return self

    def button_press(self, button):
        if button == pygame.K_ESCAPE:
            self.game.state = GamePauseState(self.game, self)
        for key in self.player.control.buttons:
            if key == button:
                self.player.control.get_action(key).start(self.player)

    def button_release(self, button):
        for key in self.player.control.buttons:
            if key == button:
                self.player.control.get_action(key).end(self.player)

    def on_click(self, screen_pos):
        direction = pygame.math.Vector2(screen_pos[0] - self.player.rect.centerx + self.world.camera.x,
                                        screen_pos[1] - self.player.rect.centery + self.world.camera.y).normalize()
        self.player.shoot(direction)


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
        return self

    def button_press(self, button):
        if button == pygame.K_ESCAPE:
            self.game.state = self.prev_state

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
        return self

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
