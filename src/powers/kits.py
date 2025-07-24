from powers.skills.light_skills import HolySpear, LuminousPulse
import pygame
from settings import *


class LightKit:
    def __init__(self, player):
        self.player = player
        self.last_spear_time = 0
        self.last_pulse_time = 0

    def activate_skill_1(self, projectile_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spear_time > HOLY_SPEAR_COOLDOWN:

            mouse_pos = pygame.mouse.get_pos()
            start_pos = self.player.pos
            direction = pygame.math.Vector2(
                mouse_pos) - pygame.math.Vector2(start_pos)

            if direction.length() > 0:
                new_spear = HolySpear(start_pos, direction)
                projectile_group.add(new_spear)

            self.last_spear_time = current_time

    def activate_skill_2(self, effect_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pulse_time > PULSE_COOLDOWN:
            new_pulse = LuminousPulse(self.player)
            effect_group.add(new_pulse)
            self.last_pulse_time = current_time
