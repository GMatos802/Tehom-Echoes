import pygame
import math
from settings import *


class Shockwave(pygame.sprite.Sprite):
    def __init__(self, start_pos, direction):
        super().__init__()

        self.original_image = pygame.Surface((400, 30), pygame.SRCALPHA)
        self.original_image.fill((BLUE))

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


class HomingSwarm(pygame.sprite.Sprite):
    def __init__(self, start_pos, player):
        super().__init__()

        self.player = player
        self.image = pygame.Surface((12, 12))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=start_pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 6

        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.spawn_time > SWARM_LIFETIME:
            self.kill()
            return

        direction = self.player.pos - self.pos

        if direction.length() > 0:
            self.pos += direction.normalize() * self.speed

        self.rect.center = self.pos

        if not pygame.Rect(0, 0, WIDTH, HEIGHT).colliderect(self.rect):
            self.kill()
