import pygame
import sys

pygame.init()

from scripts.objects import Player
from scripts.objects import Ground
from scripts.camera import Camera
from scripts.UI import UIManager

from scripts.settings import *

pygame.display.set_caption(TITLE)

blocks = [
    Ground(-100, WINDOW_HEIGHT - 50, WINDOW_WIDTH + 200, 10)
]

class Game:
    def __init__(self):
        self.startscreen = StartScreen()
        self.gameover = GameOverScreen()

        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 32, 32)
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.uimanager = UIManager()
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return False
        return True

    def update(self):

        keys = pygame.key.get_pressed()

        self.player.handle_events(keys)

        self.player.update(blocks)

        self.camera.follow(self.player)

    def render(self, surf):
        surf.fill((0, 0, 0))

        for block in blocks:
            block.render(surf, self.camera)

        self.player.render(surf, self.camera)

    def run(self):
        running = True

        while running:
            
            running = self.handle_events(pygame.event.get())

            self.update()
            self.render(SCREEN)

            pygame.display.update()
            CLOCK.tick(60)

class StartScreen:
    def __init__(self):
        pass

class GameOverScreen:
    def __init__(self):
        pass

if __name__ == "__main__":
    game = Game()

    game.run()