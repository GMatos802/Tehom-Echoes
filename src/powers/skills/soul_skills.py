import pygame
from powers.base_skill import BaseSkill
from settings import *
import math 

class SpectralScythe(BaseSkill):
    def __init__(self, pos, size, duration, direction):
        super().__init__()
        self.enemies_hit = []

        self.original_image = pygame.Surface(size, pygame.SRCALPHA)
        self.original_image.fill((0, 0, 255, 155)) 
        
        self.rect = self.original_image.get_rect(center=pos)

        angle_rad = math.atan2(direction.y, direction.x)
        angle_deg = math.degrees(angle_rad)
        self.image = pygame.transform.rotate(self.original_image, -angle_deg)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        self.spawn_time = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()

class SoulBurst(BaseSkill):
    def __init__(self, pos, radius, damage, duration):
        super().__init__()
        self.enemies_hit = []
        
        self.pos = pos
        self.radius = radius
        self.damage = damage 

        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

        self.spawn_time = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        progress = (pygame.time.get_ticks() - self.spawn_time) / self.duration
        current_radius = self.radius * (1 - progress)
        
        self.image.fill((0,0,0,0)) 
        if current_radius > 0:
            pygame.draw.circle(self.image, BLUE, (self.radius, self.radius), current_radius)

        if progress >= 1:
            self.kill()

class SoulShard(BaseSkill):
    def __init__(self, start_pos, target):
        super().__init__()
        self.enemies_hit = []
        self.target = target 
        
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE) 
        self.rect = self.image.get_rect(center = start_pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = SOUL_SHARD_SPEED

    def update(self):

        if self.target:
            direction = self.target.pos - self.pos
            if direction.length() > 0:
                self.pos += direction.normalize() * self.speed
                self.rect.center = self.pos

        if not pygame.Rect(0, 0, WIDTH, HEIGHT).colliderect(self.rect):
            self.kill()