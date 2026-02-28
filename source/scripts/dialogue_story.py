import pygame

from data.dialogues.dialogue_data import DIALOGUES
from scripts.UI import UIManager
from scripts.settings import *

class DialogueSystem:
    def __init__(self):
        self.uimanager = UIManager()

        self.active = False
        self.current_line = []
        self.index = 0

        self.speaker_label = None
        self.text_label = None

    def start_dialogue(self, dialogue_id):

        self.uimanager.clear()

        self.current_line = DIALOGUES[dialogue_id]
        self.index = 0
        self.active = True

        self.speaker_label = self.uimanager.new_hud_textlabel(
            20,
            525,
            "",
            FONT,
            (0, 0, 25),
            "left"
        )

        self.text_label = self.uimanager.new_hud_textbutton(
            WINDOW_WIDTH // 2,
            (WINDOW_HEIGHT // 2 + WINDOW_HEIGHT // 4) + 65,
            WINDOW_WIDTH - 50,
            WINDOW_HEIGHT // 4,
            "",
            FONT,
            (0, 0, 0),
            (217, 87, 116),
            "left"
        )

        self.update_line()

    def update_line(self):
        if self.index < len(self.current_line):
            line = self.current_line[self.index]
            self.speaker_label.set_text(line["speaker"])
            self.text_label.set_text(line["text"])

    def next(self):
        self.index += 1

        if self.index >= len(self.current_line):
            self.end()
        else:
            self.update_line()

    def end(self):
        self.active = False
        self.uimanager.clear()

    def update(self, events):
        if not self.active:
            return
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next()
    
    def render(self, surf):
        if self.active:
            self.uimanager.render(surf)

class StoryManager:
    def __init__(self, game):
        self.game = game
        self.step = 0

    def reset(self):
        self.step = 0

    def trigger(self, event_name):

        if self.step == 0:
            self.game.dialogue.start_dialogue("intro")
            self.step = 1
            return
        
        if self.step == 1 and event_name == "teste":
            self.game.dialogue.start_dialogue("pos-intro")
            self.step = 2
            return
        