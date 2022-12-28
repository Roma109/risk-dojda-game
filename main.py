import pygame

import main_menu
from renderer import Camera, Renderer


class Game:

    def __init__(self):
        # При инициализации клиента начинается игра
        self.width = None
        self.height = None
        self.state = MainMenuState(self)
        self.heartbeat = GameHeartbeat(self)
        self.screen = None
        self.renderer = Renderer()

    def start(self):
        pygame.init()
        pygame.display.set_caption("Риск дождя")
        display_info = pygame.display.Info()
        self.width = display_info.current_w
        self.height = display_info.current_h
        self.screen = pygame.display.set_mode((display_info.current_w, display_info.current_h))
        self.heartbeat.start()

    def update(self):
        self.state = self.state.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.heartbeat.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.on_click(event)

    def on_click(self, event):
        self.state.on_click(event.pos)

    def close(self):
        self.heartbeat.stop()
        pygame.display.quit()
        pygame.quit()


class GameHeartbeat:

    def __init__(self, game):
        self.client = game
        self.clock = pygame.time.Clock()
        self.running = False

    def start(self):
        if self.running:
            raise RuntimeError('Heartbeat has already started!')
        self.running = True
        while self.running:
            self.client.update()
            self.clock.tick(30)

    def stop(self):
        self.running = False


class GameState:

    def __init__(self, game):
        self.game = game

    def update(self):
        return MainMenuState(self.game)

    def on_click(self, screen_pos):
        pass


class MainMenuState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.world = main_menu.load_menu()
        self.camera = Camera()

    def update(self):
        #background = pygame.transform.scale(pygame.image.load('assets/main_menu/background.jpg'),
                                            #(self.game.width, self.game.height))
        #self.game.screen.blit(background, (0, 0))
        self.world.update()
        self.game.renderer.render(self.camera, self.game.screen, self.world)
        return self

    def on_click(self, screen_pos):

        game_pos = (screen_pos[0] + self.camera.x, screen_pos[1] - self.camera.y)
        clicked_obj = self.world.get_obj(game_pos)
        if clicked_obj is None:
            return
        clicked_obj.click(screen_pos, game_pos)


class GameInProgressState(GameState):

    def __init__(self, game):
        super().__init__(game)
        # TODO: загрузить уровень


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
