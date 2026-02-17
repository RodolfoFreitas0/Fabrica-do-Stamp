import pygame
import sys
import os

import json

pygame.init()

from scripts.objects import Ground
from scripts.camera import Camera
from scripts.UI import UIManager

from scripts.settings import *

pygame.display.set_caption("Editor")

class Principal:
    def __init__(self):
        self.state = "menu"
        self.menu = Menu(self)
        self.editor = Editor(self)
        self.map_list = None
    
    def run(self):
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.state == "menu":
                self.menu.update(events)
                self.menu.render(SCREEN)
            
            elif self.state == "editor":
                self.editor.update(events, pygame.key.get_pressed())
                self.editor.render(SCREEN)

            elif self.state == "map_list":
                self.map_list.update(events)
                self.map_list.render(SCREEN)

            pygame.display.update()
            CLOCK.tick(60)

class Menu:
    def __init__(self, game):
        self.game = game
        self.uimanager = UIManager()

        self.newbutton = self.uimanager.new_ui_textbutton(
            WINDOW_WIDTH // 2, 300, 400, 60,
            "Novo Mapa",
            FONT,
            self.new_map
        )

        self.loadbutton = self.uimanager.new_ui_textbutton(
            WINDOW_WIDTH // 2, 400, 400, 60,
            "Carregar Mapa",
            FONT,
            self.open_map_list
        )

        self.quitbutton = self.uimanager.new_ui_textbutton(
            WINDOW_WIDTH // 2, 500, 400, 60,
            "Sair",
            FONT,
            self.quit
        )
    
    def new_map(self):
        filename = generate_new_map_name()
        self.game.editor.current_map_name = filename
        self.game.editor.tiles.clear()
        save_map(filename, [])
        self.game.state = "editor"
    
    def open_map_list(self):
        self.game.map_list = MapList(self.game)
        self.game.state = "map_list"

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self, events):
        self.uimanager.update(events)

    def render(self, surf):
        surf.fill((0, 0, 0))
        self.uimanager.render(surf)

class MapList:
    def __init__(self, game):
        self.game = game
        self.uimanager = UIManager()

        folder = "custom_maps"
        os.makedirs(folder, exist_ok=True)

        files = sorted(os.listdir(folder))

        y = 150
        x = 250
        for file in files:
            if file.endswith(".json"):
                self.uimanager.new_ui_textbutton(
                    x, y, 400, 50,
                    file,
                    FONT,
                    lambda f=file: self.load_map(f)
                )
                y += 70
                if y >= WINDOW_HEIGHT - 50:
                    y = 150
                    x += 500
        
        self.uimanager.new_ui_textbutton(
            120, 50, 200, 50,
            "Voltar",
            FONT,
            self.go_back
        )

    def load_map(self, filename):
        load_map(filename, self.game.editor.tiles)
        self.game.editor.current_map_name = filename
        self.game.state = "editor"

    def go_back(self):
        self.game.state = "menu"
    
    def update(self, events):
        self.uimanager.update(events)

    def render(self, surf):
        surf.fill((20, 20, 20))
        self.uimanager.render(surf)

class Editor:
    def __init__(self, game):
        self.game = game
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.uimanager = UIManager()

        self.uimanager.new_ui_textbutton(
            120, 50, 200, 50,
            "Voltar",
            FONT,
            self.go_back
        )

        self.tile_size = 32
        self.tiles = []
        self.camera_speed = 8
        self.current_map_name = None
    
    def go_back(self):
        save_map(self.current_map_name, self.tiles)
        self.game.state = "menu"
    
    def update(self, events, keys):
        self.uimanager.update(events)

        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()

        world_x = mouse_pos_x + self.camera.pos.x
        world_y = mouse_pos_y + self.camera.pos.y  

        grid_x = (world_x // self.tile_size) * self.tile_size
        grid_y = (world_y // self.tile_size) * self.tile_size

        for event in events:
            if event.type == pygame.QUIT:
                save_map(self.current_map_name, self.tiles)
                self.game.state = "menu"
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    exists = False

                    for tile in self.tiles:
                        if tile.rect.x == grid_x and tile.rect.y == grid_y:
                            exists = True
                            break
                    
                    if not exists:
                        self.tiles.append(
                            Ground(grid_x, grid_y, self.tile_size, self.tile_size)
                        )
                
                if event.button == 3:

                    self.tiles = [
                        tile for tile in self.tiles
                        if not (tile.rect.x == grid_x and tile.rect.y == grid_y)
                    ]
                
        if keys[pygame.K_a]:
            self.camera.pos.x -= self.camera_speed

        if keys[pygame.K_d]:
            self.camera.pos.x += self.camera_speed

        if keys[pygame.K_w]:
            self.camera.pos.y -= self.camera_speed

        if keys[pygame.K_s]:
            self.camera.pos.y += self.camera_speed
        
        if keys[pygame.K_o] and self.current_map_name:
            save_map(self.current_map_name, self.tiles)

    def render(self, surf):
        surf.fill((0, 0, 0))

        for tile in self.tiles:
            tile.render(surf, self.camera)

        offset_x = -self.camera.pos.x % self.tile_size
        offset_y = -self.camera.pos.y % self.tile_size

        for x in range(-self.tile_size, WINDOW_WIDTH + self.tile_size, self.tile_size):
            pygame.draw.line(
                surf,
                (50, 50, 50),
                (x + offset_x, 0),
                (x + offset_x, WINDOW_HEIGHT)
            )

        for y in range(-self.tile_size, WINDOW_HEIGHT + self.tile_size, self.tile_size):
            pygame.draw.line(
                surf,
                (50, 50, 50),
                (0, y + offset_y),
                (WINDOW_WIDTH, y + offset_y)
            )

        self.uimanager.render(surf)

    def run(self):
        running = True

        while running:
            keys = pygame.key.get_pressed()
            events = pygame.event.get()
            running = self.update(events, keys)
            
            self.render(SCREEN)

            pygame.display.update()
            CLOCK.tick(60)

def save_map(filename, tiles):
    folder = "custom_maps"
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, filename)
    
    data = []

    for tile in tiles:
        data.append({
            "x": tile.rect.x,
            "y": tile.rect.y,
            "width": tile.rect.width,
            "height": tile.rect.height
        })
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def load_map(filename, tile_list):
    folder = "custom_maps"
    file_path = os.path.join(folder, filename)

    tile_list.clear()

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        
        for tile_data in data:
            tile = Ground(
                tile_data["x"],
                tile_data["y"],
                tile_data["width"],
                tile_data["height"]
            )
            tile_list.append(tile)
    except FileNotFoundError:
        pass

def generate_new_map_name():
    folder = "custom_maps"
    os.makedirs(folder, exist_ok=True)

    existing = os.listdir(folder)

    numbers = []

    for file in existing:
        if file.startswith("map_") and file.endswith(".json"):
            num = file[4:-5]
            if num.isdigit():
                numbers.append(int(num))
    
    if numbers:
        next_number = max(numbers) + 1
    else:
        next_number = 1
    
    return f"map_{next_number:03}.json"

if __name__ == "__main__":
    game = Principal()

    game.run()