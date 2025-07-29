# src/ui/hud.py

import pygame
from settings import *
from powers.kits import LightKit, FuryKit, SoulKit

class HUD:
    def __init__(self, player, enemies_group):
        self.player = player
        self.enemies = enemies_group

    def draw_player_health(self, surface):
        health_ratio = self.player.health / self.player.max_health
        current_health_width = HEALTH_BAR_WIDTH * health_ratio
        
        background_rect = pygame.Rect(HEALTH_BAR_POS[0], HEALTH_BAR_POS[1], HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
        current_health_rect = pygame.Rect(HEALTH_BAR_POS[0], HEALTH_BAR_POS[1], current_health_width, HEALTH_BAR_HEIGHT)

        pygame.draw.rect(surface, HEALTH_BACKGROUND_COLOR, background_rect)
        pygame.draw.rect(surface, HEALTH_COLOR, current_health_rect)

    def draw_boss_health(self, surface):
        if self.enemies:
            boss = self.enemies.sprites()[0]
            health_ratio = boss.health / boss.max_health
            current_health_width = BOSS_HEALTH_BAR_WIDTH * health_ratio
            
            background_rect = pygame.Rect(BOSS_HEALTH_BAR_POS[0], BOSS_HEALTH_BAR_POS[1], BOSS_HEALTH_BAR_WIDTH, BOSS_HEALTH_BAR_HEIGHT)
            current_health_rect = pygame.Rect(BOSS_HEALTH_BAR_POS[0], BOSS_HEALTH_BAR_POS[1], current_health_width, BOSS_HEALTH_BAR_HEIGHT)

            pygame.draw.rect(surface, (50,50,50), background_rect)
            pygame.draw.rect(surface, BOSS_HEALTH_COLOR, current_health_rect)

    def draw_cooldowns(self, surface):
        kit = self.player.kit
        current_time = pygame.time.get_ticks()

        if isinstance(kit, LightKit):
            self.draw_cooldown_icon(surface, 0, kit.last_spear_time, kit.current_spear_cooldown, YELLOW)
            self.draw_cooldown_icon(surface, 1, kit.last_pulse_time, PULSE_COOLDOWN, YELLOW)
        
        elif isinstance(kit, FuryKit):
            self.draw_cooldown_icon(surface, 0, 0, 1, RED)
            self.draw_cooldown_icon(surface, 1, kit.last_rush_time, kit.current_rush_cooldown, RED)
            
        elif isinstance(kit, SoulKit):
            self.draw_cooldown_icon(surface, 0, kit.last_burst_time, SOUL_BURST_COOLDOWN, BLUE)
            self.draw_cooldown_icon(surface, 1, kit.last_scythe_time, SCYTHE_COOLDOWN, BLUE)

    def draw_cooldown_icon(self, surface, index, last_use_time, cooldown, color):
        elapsed_time = pygame.time.get_ticks() - last_use_time

        if cooldown > 0:
            progress_ratio = min(elapsed_time / cooldown, 1.0)
        else:
            progress_ratio = 1.0

        pos_x = COOLDOWN_ICON_POS[0] + index * (COOLDOWN_ICON_SIZE + COOLDOWN_ICON_PADDING)
        pos_y = COOLDOWN_ICON_POS[1]

        bg_rect = pygame.Rect(pos_x, pos_y, COOLDOWN_ICON_SIZE, COOLDOWN_ICON_SIZE)
        pygame.draw.rect(surface, COOLDOWN_BG_COLOR, bg_rect, border_radius=8)

        if progress_ratio < 1.0:
            fill_height = COOLDOWN_ICON_SIZE * progress_ratio
            fill_rect = pygame.Rect(pos_x, pos_y + COOLDOWN_ICON_SIZE - fill_height, COOLDOWN_ICON_SIZE, fill_height)
            
            temp_surface = pygame.Surface(fill_rect.size, pygame.SRCALPHA)
            temp_surface.fill(color)
            surface.blit(temp_surface, fill_rect.topleft)

        pygame.draw.rect(surface, color, bg_rect, width=3, border_radius=8)


    def draw(self, surface):
        self.draw_player_health(surface)
        self.draw_boss_health(surface)
        self.draw_cooldowns(surface)