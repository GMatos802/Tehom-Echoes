import pygame
from powers.base_skill import BaseSkill
from settings import *
import math


class HolySpear(BaseSkill):
    def __init__(self, start_pos, direction):
        super().__init__()

        self.enemies_hit = []

        self.original_image = pygame.Surface((60, 20), pygame.SRCALPHA)
        self.original_image.fill(YELLOW)

        angle_rad = math.atan2(direction.y, direction.x)
        angle_deg = math.degrees(angle_rad)
        self.image = pygame.transform.rotate(self.original_image, -angle_deg)

        self.rect = self.image.get_rect(center=start_pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.velocity = direction.normalize() * 30

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

        if not pygame.Rect(0, 0, WIDTH, HEIGHT).colliderect(self.rect):
            self.kill()


class LuminousPulse(BaseSkill):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.radius = 0
        self.max_radius = PULSE_RADIUS
        self.duration = PULSE_DURATION
        self.spawn_time = pygame.time.get_ticks()
        self.enemies_hit = []

        self.image = pygame.Surface(
            (self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=player.rect.center)

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        if elapsed_time > self.duration:
            self.kill()
            return

        self.radius = (elapsed_time / self.duration) * self.max_radius

        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, YELLOW, (self.max_radius,
                           self.max_radius), self.radius, width=5)

        self.rect.center = self.player.rect.center
