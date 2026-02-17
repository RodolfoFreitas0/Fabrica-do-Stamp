import pygame

class Face():
    def __init__(self, head_size, eye_size, mouth_size):
        self.head_size = head_size
        self.eye_size = eye_size
        self.mouth_size = mouth_size

    def render(self, surf, center, velocity, camera):
        centerx, centery = center

        centerx -= camera.pos.x
        centery -= camera.pos.y

        eye_offset_x = self.head_size // 4
        eye_offset_y = self.head_size // 4

        direction = pygame.Vector2(velocity)

        if direction.length() > 0:
            direction = direction.normalize()
        else:
            direction = pygame.Vector2(0, 0)
        
        pupil_offset_strength = self.eye_size // 2

        pupil_offset = direction * pupil_offset_strength

        left_eye_center = pygame.Vector2(
            centerx - eye_offset_x,
            centery + eye_offset_y
        )

        pygame.draw.circle(
            surf,
            (255, 255, 255),
            left_eye_center,
            self.eye_size
        )

        pygame.draw.circle(
            surf,
            (0, 0, 0),
            left_eye_center + pupil_offset,
            self.eye_size // 2
        )

        right_eye_center = pygame.Vector2(
            centerx + eye_offset_x,
            centery + eye_offset_y
        )

        pygame.draw.circle(
            surf,
            (255, 255, 255),
            right_eye_center,
            self.eye_size
        )

        pygame.draw.circle(
            surf,
            (0, 0, 0),
            right_eye_center + pupil_offset,
            self.eye_size // 2
        )


        # pygame.draw.rect(surf, (255, 255, 255),
        #                 (int(centerx - self.mouth_size // 2),
        #                 int(centery + self.head_size // 2),
        #                 self.mouth_size,
        #                 1)
        #                 )