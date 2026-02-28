import pygame
import sys
import os
import json

pygame.init()

from scripts.screens import StartScreen, GameOverScreen, CutsceneScreen, GameScreen, VictoryScreen
from scripts.settings import *

pygame.display.set_caption(TITLE)

class Game:
    def __init__(self):

        self.screens = {
            "start": StartScreen(self),
            "game": GameScreen(self),
            "cutscene": CutsceneScreen(self),
            "gameover": GameOverScreen(self),
            "victory": VictoryScreen(self)
        }

        self.state = "start"

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    return False
        return True
    
    def change_state(self, new_state):
        if new_state in self.screens:
            self.state = new_state

    def current_screen(self):
        return self.screens[self.state]

    def update(self, events):
        self.current_screen().update(events)

    def render(self, surf):
        surf.fill((0, 0, 0))
        self.current_screen().render(surf)

    def run(self):
        running = True

        while running:       
            events = pygame.event.get()

            self.handle_events(events)
            self.update(events)
            self.render(SCREEN)

            pygame.display.update()
            CLOCK.tick(60)

if __name__ == "__main__":
    game = Game()

    game.run()