import pygame
from settings import *
from powers.kits import LightKit, FuryKit, SoulKit
from entities.characters.caim import Caim

class HUD:
    def __init__(self, player, enemies_group):
        self.player = player
        self.enemies = enemies_group
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 18)

    def draw_player_health(self, surface):
        if self.player.max_health > 0:
            health_ratio = self.player.health / self.player.max_health
            current_health_width = HEALTH_BAR_WIDTH * health_ratio
            
            background_rect = pygame.Rect(HEALTH_BAR_POS[0], HEALTH_BAR_POS[1], HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
            current_health_rect = pygame.Rect(HEALTH_BAR_POS[0], HEALTH_BAR_POS[1], current_health_width, HEALTH_BAR_HEIGHT)

            pygame.draw.rect(surface, HEALTH_BACKGROUND_COLOR, background_rect)
            pygame.draw.rect(surface, HEALTH_COLOR, current_health_rect)

    def draw_boss_health(self, surface):
        if self.enemies:
            boss = self.enemies.sprites()[0]
            if hasattr(boss, 'max_health') and boss.max_health > 0:
                health_ratio = boss.health / boss.max_health
                current_health_width = BOSS_HEALTH_BAR_WIDTH * health_ratio
                
                bar_x = WIDTH / 2 - BOSS_HEALTH_BAR_WIDTH / 2
                bar_y = 55
                
                background_rect = pygame.Rect(bar_x, bar_y, BOSS_HEALTH_BAR_WIDTH, BOSS_HEALTH_BAR_HEIGHT)
                pygame.draw.rect(surface, (50, 50, 50), background_rect)

                if current_health_width > 0:
                    current_health_rect = pygame.Rect(bar_x, bar_y, current_health_width, BOSS_HEALTH_BAR_HEIGHT)
                    pygame.draw.rect(surface, BOSS_HEALTH_COLOR, current_health_rect)

    def draw_cooldowns(self, surface):
        kit = self.player.kit
        
        if isinstance(kit, LightKit):
            self.draw_cooldown_icon(surface, 0, kit.last_spear_time, kit.current_spear_cooldown, YELLOW)
            self.draw_cooldown_icon(surface, 1, kit.last_pulse_time, kit.current_pulse_cooldown, YELLOW)
        
        elif isinstance(kit, FuryKit):
            self.draw_cooldown_icon(surface, 0, 0, 1, RED) # Combo não tem cooldown
            self.draw_cooldown_icon(surface, 1, kit.last_rush_time, kit.current_rush_cooldown, RED)
            
        elif isinstance(kit, SoulKit):
            self.draw_cooldown_icon(surface, 0, kit.last_burst_time, kit.current_burst_cooldown, BLUE)
            self.draw_cooldown_icon(surface, 1, kit.last_scythe_time, kit.current_scythe_cooldown, BLUE)

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

        if progress_ratio < 1.0:
            remaining_time = (cooldown - elapsed_time) / 1000
            text = f"{max(0, remaining_time):.4f}" 
            text_surface = self.small_font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=bg_rect.center)
            surface.blit(text_surface, text_rect)

        if isinstance(self.player, Caim) and cooldown > 1:
            total_cooldown_text = f"{cooldown / 1000:.4f}s"
            total_cd_surface = self.tiny_font.render(total_cooldown_text, True, (200, 200, 200)) 
            total_cd_rect = total_cd_surface.get_rect(topright=(bg_rect.right - 5, bg_rect.top + 5))
            surface.blit(total_cd_surface, total_cd_rect)

    def draw_passives(self, surface):
        if isinstance(self.player, Caim):
            bg_rect = pygame.Rect(PASSIVE_ICON_POS[0], PASSIVE_ICON_POS[1], PASSIVE_ICON_SIZE, PASSIVE_ICON_SIZE)
            pygame.draw.rect(surface, PASSIVE_BG_COLOR, bg_rect, border_radius=8)
            
            damage_multiplier = self.player.get_damage_multiplier()
            bonus_percent = int((damage_multiplier - 1) * 100)
            
            text = f"+{bonus_percent}%"
            text_surface = self.small_font.render(text, True, CAIM_PASSIVE_COLOR)
            text_rect = text_surface.get_rect(center=bg_rect.center)
            surface.blit(text_surface, text_rect)
            
            pygame.draw.rect(surface, CAIM_PASSIVE_COLOR, bg_rect, width=3, border_radius=8)

    def draw(self, surface):
        self.draw_player_health(surface)
        self.draw_boss_health(surface)
        self.draw_cooldowns(surface)
        self.draw_passives(surface)