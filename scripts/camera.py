import pygame

class Camera:
    def __init__(self, width, height):
        self.pos = pygame.Vector2(0, 0)

        self.width = width
        self.height = height

    def follow(self, target):
        self.pos.x = target.rect.centerx - self.width // 2
        self.pos.y = target.rect.centery - self.height // 2

    def apply(self, rect):
        return rect.move(-self.pos.x, -self.pos.y)