from powers.skills.light_skills import HolySpear, LuminousPulse
from powers.skills.fury_skills import Slash, UnstoppableRush, RushHitbox
import pygame
from settings import *


class LightKit:
    def __init__(self, player):
        self.player = player
        self.last_spear_time = 0
        self.last_pulse_time = 0
        self.current_spear_cooldown = HOLY_SPEAR_BASE_COOLDOWN

    def activate_skill_1(self, projectile_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spear_time > self.current_spear_cooldown:
            mouse_pos = pygame.mouse.get_pos()
            start_pos = self.player.pos
            direction = pygame.math.Vector2(
                mouse_pos) - pygame.math.Vector2(start_pos)

            if direction.length() > 0:
                new_spear = HolySpear(start_pos, direction)
                projectile_group.add(new_spear)

            self.last_spear_time = current_time

    def on_spear_hit(self):
        self.current_spear_cooldown -= HOLY_SPEAR_COOLDOWN_REDUCTION
        if self.current_spear_cooldown < HOLY_SPEAR_MIN_COOLDOWN:
            self.current_spear_cooldown = HOLY_SPEAR_MIN_COOLDOWN
        print(f"Novo cooldown da Lança: {self.current_spear_cooldown}ms")

    def activate_skill_2(self, effect_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pulse_time > PULSE_COOLDOWN:
            new_pulse = LuminousPulse(self.player)
            effect_group.add(new_pulse)
            self.last_pulse_time = current_time


class FuryKit:
    def __init__(self, player):
        self.player = player

        self.combo_step = 0
        self.last_slash_time = 0

        self.last_rush_time = -RUSH_COOLDOWN
        self.current_rush_cooldown = RUSH_COOLDOWN
        self.is_rushing = False
        self.rush_end_time = 0
        self.rush_direction = pygame.math.Vector2()
        self.rush_hitbox = None 

    def activate_skill_1(self, player_attack_group):
        current_time = pygame.time.get_ticks()

        if self.combo_step > 0 and current_time - self.last_slash_time > COMBO_WINDOW:
            self.combo_step = 0
        
        self.combo_step += 1
        self.last_slash_time = current_time

        mouse_pos = pygame.mouse.get_pos()
        player_pos = self.player.pos
        direction = (pygame.math.Vector2(mouse_pos) - player_pos).normalize()

        slash_pos = player_pos + direction * 40

        if self.combo_step == 1:
            new_slash = Slash(slash_pos, SLASH_HITBOX_SIZE, 100, direction)
            player_attack_group.add(new_slash)
        
        elif self.combo_step == 2:
            new_slash = Slash(slash_pos, SLASH_HITBOX_SIZE, 100, direction)
            player_attack_group.add(new_slash)
        
        elif self.combo_step == 3:
            final_slash_size = (SLASH_HITBOX_SIZE[0] * 1.5, SLASH_HITBOX_SIZE[1] * 1.5)
            new_slash = Slash(slash_pos, final_slash_size, 200, direction)
            player_attack_group.add(new_slash)
            self.combo_step = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.combo_step > 0 and current_time - self.last_slash_time > COMBO_WINDOW:
            self.combo_step = 0

        if self.is_rushing and current_time > self.rush_end_time:
            if self.rush_hitbox:
                self.rush_hitbox.kill()
                self.rush_hitbox = None

    def activate_skill_2(self, player_attack_group):
        current_time = pygame.time.get_ticks()

        if not self.is_rushing and current_time - self.last_rush_time > self.current_rush_cooldown:
            self.is_rushing = True

            mouse_pos = pygame.mouse.get_pos()
            player_pos = self.player.pos
            self.rush_direction = (pygame.math.Vector2(
                mouse_pos) - player_pos).normalize()

            self.rush_end_time = current_time + RUSH_DURATION
            self.last_rush_time = current_time

            self.rush_hitbox = RushHitbox(self.player)
            player_attack_group.add(self.rush_hitbox)

    def on_slash_hit(self):
        self.current_rush_cooldown -= RUSH_COOLDOWN_REDUCTION_ON_HIT
        if self.current_rush_cooldown < 0:
            self.current_rush_cooldown = 0
        print(f"Novo cooldown do rush: {self.current_rush_cooldown}ms")
