import pygame
from settings import *


class DummyEnemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((RED))
        self.rect = self.image.get_rect(center=pos)
        self.health = 10

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
