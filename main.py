import pygame

import level
import main_menu
from camera import ObjectFollowMode
from player import Player


class Game:

    def __init__(self):
        self.state = GameState(self)
        self.heartbeat = GameHeartbeat(self)
        self.screen = None
        self.display_info = None

    def start(self):
        pygame.init()
        pygame.display.set_caption("Риск дождя")
        self.display_info = pygame.display.Info()
        self.width = self.display_info.current_w
        self.height = self.display_info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.heartbeat.start()

    def update(self):
        self.state = self.state.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.heartbeat.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.state.on_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.state.button_press(event.key)
            elif event.type == pygame.KEYUP:
                self.state.button_release(event.key)

    def close(self):
        self.heartbeat.stop()
        pygame.display.quit()
        pygame.quit()


class GameHeartbeat:

    def __init__(self, game):
        self.game = game
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.running = False

    def start(self):
        if self.running:
            raise RuntimeError('Heartbeat has already started!')
        self.running = True
        while self.running:
            self.game.update()
            self.clock.tick(self.fps)

    def stop(self):
        self.running = False


class GameState:

    def __init__(self, game):
        self.game = game

    def update(self):
        return MainMenuState(self.game)

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
        self.start = False

    def update(self):
        self.game.screen.fill((0, 0, 0))
        self.world.update()
        self.world.draw(self.game.screen)
        pygame.display.flip()
        if self.start:
            return GameInProgressState(self.game)
        return self

    def on_click(self, pos):
        clicked_obj = self.world.get_obj(pos)
        if clicked_obj is None or not isinstance(clicked_obj, main_menu.Button):
            return
        clicked_obj.click(pos)


class GameInProgressState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.level = level.load_level()
        self.player = Player(self.level.start_pos[0], self.level.start_pos[1],
                    self.level.world, pygame.image.load('assets/player.jpg'))
        self.level.world.add_human(self.player)
        self.level.world.camera.set_mode(ObjectFollowMode(self.player))
        print('game in progress!')

    def update(self):
        self.game.screen.fill((0, 0, 0))
        self.level.update()
        self.level.world.draw(self.game.screen)
        pygame.display.flip()
        return self

    def button_press(self, button):
        for key in self.player.control.buttons:
            if key == button:
                self.player.control.get_action(key).start(self.player)

    def button_release(self, button):
        for key in self.player.control.buttons:
            if key == button:
                self.player.control.get_action(key).end(self.player)


GAME = None


def main():
    global GAME
    pygame.init()
    pygame.font.init()
    GAME = Game()
    GAME.start()


def get_game():
    return GAME


if __name__ == '__main__':
    main()
