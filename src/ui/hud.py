import pygame
from settings import *


class HUD:
    def __init__(self, player):
        self.player = player
        self.health_bar_background_rect = pygame.Rect(
            HEALTH_BAR_POS[0],
            HEALTH_BAR_POS[1],
            HEALTH_BAR_WIDTH,
            HEALTH_BAR_HEIGHT
        )

    def draw(self, surface):
        health_ratio = self.player.health / self.player.max_health

        current_health_width = HEALTH_BAR_WIDTH * health_ratio

        current_health_rect = pygame.Rect(
            HEALTH_BAR_POS[0],
            HEALTH_BAR_POS[1],
            current_health_width,
            HEALTH_BAR_HEIGHT
        )

        pygame.draw.rect(surface, HEALTH_BACKGROUND_COLOR,
                         self.health_bar_background_rect)
        pygame.draw.rect(surface, HEALTH_COLOR, current_health_rect)
