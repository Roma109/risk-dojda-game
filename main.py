import pygame as pygame

import main_menu
from renderer import Camera


class Game:

    def __init__(self):
        # При инициализации клиента начинается игра
        self.state = TestState(self)
        self.heartbeat = GameHeartbeat(self)
        self.screen = None
        self.camera = Camera()

    def start(self):
        pygame.init()
        pygame.display.set_caption("Риск дождя")
        display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((display_info.current_w, display_info.current_h))
        self.heartbeat.start()

    def update(self):
        self.state.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.heartbeat.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.on_click(event)

    def on_click(self, event):
        self.state.on_click(event.pos)

    def close(self):
        pygame.display.quit()
        pygame.quit()


class GameHeartbeat:

    def __init__(self, client):
        self.client = client
        self.running = False

    def start(self):
        if self.running:
            raise RuntimeError('Heartbeat has already started!')
        self.running = True
        while self.running:
            # TODO: сделать ограничение фпс
            self.client.update()

    def stop(self):
        self.running = False


class TestState:

    def __init__(self, game):
        self.game = game
        self.world = main_menu.load_menu()

    def update(self):
        self.world.render(self.game.screen, self.game.camera)
        pygame.display.flip()

    def on_click(self, pos):
        clicked_obj = self.world.get_obj(pos)
        if clicked_obj is None:
            return
        clicked_obj.click(pos)


GAME = None


def main():
    global GAME
    pygame.init()
    GAME = Game()
    GAME.start()


if __name__ == '__main__':
    main()
