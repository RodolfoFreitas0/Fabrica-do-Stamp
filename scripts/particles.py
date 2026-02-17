import pygame

class Particle:
    def __init__(self, x, y, xvel, yvel, width=0, height=0, radius=0, color=(255, 255, 255), gravity=None, type="circle"):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.width = width
        self.height = height
        self.radius = radius
        self.color = color
        self.gravity = gravity
        self.type = type
    
    def update(self):
        self.yvel += self.gravity

        self.x += self.xvel
        self.y += self.yvel
    
    def render(self, surf):
        if self.type == "circle":
            pygame.draw.circle(surf, self.color, (self.x, self.y), self.radius)
        elif self.type == "rect":
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(surf, self.color, rect)

class ParticleManager:
    def __init__(self):
        self.particles = []
    
    

