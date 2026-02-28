import pygame

from data.cutscenes.cutscene_data import INTRO_CUTSCENE

from scripts.settings import *

class CutsceneManager:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.active = True
        self.scenes = INTRO_CUTSCENE
        self.index = 0
        self.current_image = None
        self.load_scene()

    def update(self, events):
        if not self.active:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.index += 1
                self.load_scene()
                break

    def load_scene(self):
        if self.index >= len(self.scenes):
            self.end()
            return
    
        scene = self.scenes[self.index]
        self.current_image = scene["image"]

        if "dialogue" in scene:
            self.screen.dialogue.start_dialogue(scene["dialogue"])


    def render(self, surf):
        if not self.active:
            return
        
        current_img_scale = pygame.transform.scale(self.current_image, (1014, 528))
        
        rect = current_img_scale.get_rect()
        rect.centerx = WINDOW_WIDTH // 2
        rect.top = 30
        
        if self.current_image:
            surf.blit(current_img_scale, rect)
    
    def end(self):
        self.index = 0
        self.active = False
        self.game.change_state("game")