import pygame


class BaseSkill(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def activate(self):
        pass
