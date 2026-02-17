import pygame

from scripts.loader import load_img
class Object():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        pass

    def render(self, surf, camera):
        pygame.draw.rect(surf, (255, 255, 255), camera.apply(self.rect))

class PhysObject(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.velocity = pygame.Vector2(0, 0)

        self.gravity = 1
        self.onground = False

    def gravity_ef(self):
        if not self.onground:
            self.velocity.y += self.gravity

    def move(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def update(self):
        self.gravity_ef()
        self.move()

class Ground(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, surf, camera):
        pygame.draw.rect(surf, (255, 255, 255), camera.apply(self.rect))

class Player(PhysObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.sprites = {
            "idle": load_img("entities/CarimboG.png"),
            "right": load_img("entities/CarimboGLado.png")
        }

        self.speed = 4
        self.jump_force = 15
        self.walking = None
    
    def handle_events(self, keys):

        self.velocity.x = 0

        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
            self.walking = "left"
        
        if keys[pygame.K_d]:
            self.velocity.x = self.speed
            self.walking = "right"
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.onground:
            self.velocity.y = -self.jump_force

    def update(self, grounds):

        if self.velocity.x == 0:
            self.walking = None

        self.onground = False

        self.gravity_ef()

        self.rect.x += self.velocity.x

        for ground in grounds:
            if self.rect.colliderect(ground.rect):
                if self.velocity.x > 0:
                    self.rect.right = ground.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = ground.rect.right
        
        self.rect.y += self.velocity.y

        for ground in grounds:
            if self.rect.colliderect(ground.rect):
                
                if self.velocity.y >= 0:
                    self.rect.bottom = ground.rect.top
                    self.velocity.y = 0
                    self.onground = True
                
                elif self.velocity.y < 0:
                    self.rect.top = ground.rect.bottom
                    self.velocity.y = 0
        
    def render(self, surf, camera):
        if self.walking == "right":
            carimboG_scaled = pygame.transform.scale(self.sprites["right"], (self.rect.width, self.rect.height))
            surf.blit(carimboG_scaled, (self.rect.x - camera.pos.x, self.rect.y - camera.pos.y))
        elif self.walking == "left":
            carimboG_scaled = pygame.transform.scale(self.sprites["right"], (self.rect.width, self.rect.height))
            carimboG_fliped = pygame.transform.flip(carimboG_scaled, True, False)
            surf.blit(carimboG_fliped, (self.rect.x - camera.pos.x, self.rect.y - camera.pos.y))
        else:
            carimboG_scaled = pygame.transform.scale(self.sprites["idle"], (self.rect.width, self.rect.height))
            surf.blit(carimboG_scaled, (self.rect.x - camera.pos.x, self.rect.y - camera.pos.y))