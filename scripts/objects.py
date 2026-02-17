import pygame

from scripts.face import Face

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

        self.stamp_rect = pygame.Rect(x - 2, y + height - 2, width + 4, 5)
        self.inv_rect = pygame.Rect(x + 2, y + height - 5, width - 4, 5)
        self.collor_rect = pygame.Rect(x, y + height + 2, width, 2)

        self.speed = 5
        self.jump_force = 15

        self.face = Face(
            head_size=width,
            eye_size=width//6,
            mouth_size=width//3
        )
    
    def handle_events(self, keys):

        self.velocity.x = 0

        if keys[pygame.K_a]:
            self.velocity.x = -self.speed
        
        if keys[pygame.K_d]:
            self.velocity.x = self.speed
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.onground:
            self.velocity.y = -self.jump_force

    def update(self, grounds):

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

        self.stamp_rect.topleft = (self.rect.x - 2, self.rect.y + self.rect.height - 2)
        self.inv_rect.topleft = (self.rect.x + 2, self.rect.y + self.rect.height - 5)
        self.collor_rect.topleft = (self.rect.x, self.rect.y + self.rect.height + 2)
        
    def render(self, surf, camera):
        pygame.draw.rect(surf, (255, 255, 255), camera.apply(self.rect), 2)

        face_center = (
            self.rect.centerx,
            self.rect.y + 5
        )

        pygame.draw.rect(surf, (0, 200, 0), camera.apply(self.collor_rect), 1)
        pygame.draw.rect(surf, (255, 255, 255), camera.apply(self.stamp_rect), 2)
        pygame.draw.rect(surf, (0, 0, 0), camera.apply(self.inv_rect), 2)

        self.face.render(surf, face_center, self.velocity, camera)