import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

NS_WINDOW_WIDTH = 320
NS_WINDOW_HEIGHT = 180

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

NS_SURFACE = pygame.Surface((NS_WINDOW_WIDTH, NS_WINDOW_HEIGHT))

CLOCK = pygame.time.Clock()

FONT = pygame.font.SysFont("MonoCraft", 32)

TITLE = "CARIMBO JOGO"