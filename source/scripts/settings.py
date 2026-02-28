import pygame
import os

pygame.init()
pygame.font.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

SCREEN = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN | pygame.SCALED)

CLOCK = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FONT_PATH = os.path.join(ROOT_DIR, "data", "fonts", "Monocraft.ttf")

if os.path.exists(FONT_PATH):
    FONT = pygame.font.Font(FONT_PATH, 20)
else:
    FONT = pygame.font.Font(None, 25)

TITLE = "CARIMBO JOGO"
pygame.display.set_caption(TITLE)