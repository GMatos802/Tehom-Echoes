import pygame
import math
from settings import *


class Shockwave(pygame.sprite.Sprite):
    def __init__(self, start_pos, direction):
        super().__init__()

        self.original_image = pygame.Surface((400, 50), pygame.SRCALPHA)
        self.original_image.fill((150, 75, 0))

        self.rect = self.original_image.get_rect(center=start_pos)

        angle_rad = math.atan2(direction.y, direction.x)
        angle_deg = math.degrees(angle_rad)

        self.image = pygame.transform.rotate(self.original_image, -angle_deg)

        self.rect = self.image.get_rect(center=self.rect.center)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.velocity = direction.normalize() * 20

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

        if not pygame.Rect(0, 0, WIDTH, HEIGHT).colliderect(self.rect):
            self.kill()
