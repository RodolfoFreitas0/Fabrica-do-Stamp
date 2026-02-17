import pygame

class Camera:
    def __init__(self, width, height):
        self.pos = pygame.Vector2(0, 0)

        self.width = width
        self.height = height

        self.smooth = 0.5

    def follow(self, target):
        target_x = target.rect.centerx - self.width // 2
        target_y = target.rect.centery - self.height // 2

        target_pos = pygame.Vector2(target_x, target_y)

        self.pos += (target_pos - self.pos) * (self.smooth / 2)

    def apply(self, rect):
        return rect.move(-self.pos.x, -self.pos.y)