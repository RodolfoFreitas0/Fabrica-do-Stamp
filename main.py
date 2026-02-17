import pygame
import sys
import os
import json
import random

pygame.init()

from scripts.objects import Player
from scripts.objects import Ground
from scripts.camera import Camera
from scripts.UI import UIManager
from scripts.particles import Particle

from scripts.settings import *

pygame.display.set_caption(TITLE)

class Game:
    def __init__(self):
        self.startscreen = StartScreen()
        self.gameover = GameOverScreen()

        self.player = Player(NS_WINDOW_WIDTH // 2, NS_WINDOW_HEIGHT // 2, 32, 32)
        self.camera = Camera(NS_WINDOW_WIDTH, NS_WINDOW_HEIGHT)
        self.uimanager = UIManager()

        self.blocks = []
        self.particles = []
    
    def load_map(self, filename):
        self.blocks = load_ofc_map(filename)

        if self.blocks:
            highest_bock = min(self.blocks, key=lambda b: b.rect.y)

            self.player.rect.x = highest_bock.rect.x
            self.player.rect.y = highest_bock.rect.y - self.player.rect.height
    
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
        self.player.update(self.blocks)
        self.camera.follow(self.player)

    def render(self, surf):
        surf.fill((20, 20, 20))

        for block in self.blocks:
            block.render(surf, self.camera)

        self.player.render(surf, self.camera)

    def run(self):
        running = True

        while running:
            
            running = self.handle_events(pygame.event.get())

            self.update()
            self.render(NS_SURFACE)

            scaled_surface = pygame.transform.scale(NS_SURFACE, (WINDOW_WIDTH, WINDOW_HEIGHT))

            SCREEN.blit(scaled_surface, (0, 0))
            pygame.display.update()
            CLOCK.tick(60)

class StartScreen:
    def __init__(self):
        pass

class GameOverScreen:
    def __init__(self):
        pass

def load_ofc_map(filename):
    folder = "maps"
    file_path = os.path.join(folder, filename)

    blocks = []

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

            for tile_data in data:
                block = Ground(
                    tile_data["x"],
                    tile_data["y"],
                    tile_data["width"],
                    tile_data["height"]
                )
                blocks.append(block)
        
    except FileNotFoundError:
        pass
    
    return blocks

if __name__ == "__main__":
    game = Game()

    game.load_map("map_001.json")

    game.run()