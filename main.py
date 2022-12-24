import os
import sys

import pygame as pygame

import main_menu
from renderer import Renderer, Camera


class Server:

    def __init__(self):
        # TODO: init world
        pass


class Client:

    def __init__(self):
        # При инициализации клиента начинается игра
        self.state = TestState(self)
        self.heartbeat = ClientHeartbeat(self)
        infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        self.camera = Camera()
        self.renderer = Renderer()
        pygame.init()
        pygame.display.set_caption("Риск дождя")
        self.heartbeat.start()

    def tick(self):
        self.state.tick()
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


class ClientHeartbeat:

    def __init__(self, client):
        self.client = client
        self.running = False

    def start(self):
        if self.running:
            raise RuntimeError('Heartbeat has already started!')
        self.running = True
        while self.running:
            self.client.tick()

    def stop(self):
        self.running = False


class TestState:

    def __init__(self, client):
        self.client = client
        self.world = main_menu.load_menu()

    def tick(self):
        self.client.renderer.render(self.world, self.client.screen, self.client.camera)
        pygame.display.flip()

    def on_click(self, pos):
        clicked_obj = self.world.get_obj(pos)
        if clicked_obj is None:
            return
        clicked_obj.click(pos)


def main():
    pygame.init()
    client = Client()


if __name__ == '__main__':
    main()
