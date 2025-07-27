import pygame
from settings import *
from powers.base_skill import BaseSkill
import math 


class Slash(BaseSkill):
    def __init__(self, pos, size, duration, direction):
        super().__init__()
        
        self.original_image = pygame.Surface(size, pygame.SRCALPHA)
        self.original_image.fill((155, 0, 0, 150)) 

        self.rect = self.original_image.get_rect(center=pos)

        angle_rad = math.atan2(direction.y, direction.x)
        angle_deg = math.degrees(angle_rad)

        self.image = pygame.transform.rotate(self.original_image, -angle_deg)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.spawn_time = pygame.time.get_ticks()
        self.duration = duration

        self.enemies_hit = []

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()


class UnstoppableRush(BaseSkill):
    def __init__(self, player):
        super().__init__()
        pass

class RushHitbox(BaseSkill):
    def __init__(self, player):
        super().__init__()
        self.enemies_hit = [] 
        self.player = player
        size = (PLAYER_WIDTH + 80, PLAYER_HEIGHT + 80)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 150)) 
        self.rect = self.image.get_rect(center=player.pos)
 
        self.spawn_time = pygame.time.get_ticks()
        self.duration = RUSH_HITBOX_DURATION

    def update(self):
        self.rect.center = self.player.rect.center

        if pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.kill() 
