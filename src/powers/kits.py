import pygame
from settings import *
from powers.skills.light_skills import HolySpear, LuminousPulse
from powers.skills.fury_skills import Slash, RushHitbox
from powers.skills.soul_skills import SpectralScythe, SoulBurst, SoulShard

class LightKit:
    def __init__(self, player):
        self.player = player
        self.last_spear_time = 0
        self.last_pulse_time = 0
        self.current_spear_cooldown = HOLY_SPEAR_BASE_COOLDOWN
        self.current_pulse_cooldown = PULSE_COOLDOWN

    def update(self):
        if self.current_spear_cooldown < HOLY_SPEAR_BASE_COOLDOWN:
            self.current_spear_cooldown += 2
        if self.current_pulse_cooldown < PULSE_COOLDOWN:
            self.current_pulse_cooldown += 2

    def activate_skill_1(self, player_attack_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spear_time > self.current_spear_cooldown:
            mouse_pos = pygame.mouse.get_pos()
            start_pos = self.player.pos
            direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(start_pos)
            if direction.length() > 0:
                new_spear = HolySpear(start_pos, direction)
                player_attack_group.add(new_spear)
            self.last_spear_time = current_time
            return True
        return False

    def on_spear_hit(self):
        self.current_spear_cooldown -= HOLY_SPEAR_COOLDOWN_REDUCTION
        if self.current_spear_cooldown < HOLY_SPEAR_MIN_COOLDOWN:
            self.current_spear_cooldown = HOLY_SPEAR_MIN_COOLDOWN

    def activate_skill_2(self, effect_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pulse_time > self.current_pulse_cooldown:
            new_pulse = LuminousPulse(self.player)
            effect_group.add(new_pulse)
            self.last_pulse_time = current_time
            return True
        return False

    def reduce_cooldowns(self, skill_number):
        if skill_number == 1:
            self.current_pulse_cooldown -= CAIM_COOLDOWN_REDUCTION
            if self.current_pulse_cooldown < 200: self.current_pulse_cooldown = 200
        elif skill_number == 2:
            self.current_spear_cooldown -= CAIM_COOLDOWN_REDUCTION
            if self.current_spear_cooldown < HOLY_SPEAR_MIN_COOLDOWN: self.current_spear_cooldown = HOLY_SPEAR_MIN_COOLDOWN

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

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.combo_step > 0 and current_time - self.last_slash_time > COMBO_WINDOW:
            self.combo_step = 0
        if self.is_rushing and current_time > self.rush_end_time:
            if self.rush_hitbox:
                self.rush_hitbox.kill()
                self.rush_hitbox = None

    def activate_skill_1(self, player_attack_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_slash_time > COMBO_WINDOW:
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
        return True

    def activate_skill_2(self, player_attack_group):
        current_time = pygame.time.get_ticks()
        if not self.is_rushing and current_time - self.last_rush_time > self.current_rush_cooldown:
            self.is_rushing = True
            mouse_pos = pygame.mouse.get_pos()
            player_pos = self.player.pos
            self.rush_direction = (pygame.math.Vector2(mouse_pos) - player_pos).normalize()
            self.rush_end_time = current_time + RUSH_DURATION
            self.last_rush_time = current_time
            self.rush_hitbox = RushHitbox(self.player)
            player_attack_group.add(self.rush_hitbox)
            return True
        return False

    def on_slash_hit(self):
        self.current_rush_cooldown -= RUSH_COOLDOWN_REDUCTION_ON_HIT
        if self.current_rush_cooldown < 0:
            self.current_rush_cooldown = 0

    def reduce_cooldowns(self, skill_number):
        if skill_number == 1:
            self.current_rush_cooldown -= CAIM_COOLDOWN_REDUCTION
            if self.current_rush_cooldown < 0: self.current_rush_cooldown = 0
        elif skill_number == 2:
            pass

class SoulKit:
    def __init__(self, player):
        self.player = player
        self.last_scythe_time = -SCYTHE_COOLDOWN
        self.is_charging = False
        self.charge_start_time = 0
        self.current_charge_time = SOUL_BURST_INITIAL_CHARGE_TIME
        self.last_burst_time = -SOUL_BURST_COOLDOWN
        self.scythe_stacks = 0
        self.last_scythe_hit_time = 0
        self.last_shard_time = 0
        self.current_scythe_cooldown = SCYTHE_COOLDOWN
        self.current_burst_cooldown = SOUL_BURST_COOLDOWN

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.scythe_stacks > 0 and current_time - self.last_scythe_hit_time > SCYTHE_STACK_DURATION:
            self.scythe_stacks = 0
        if self.is_charging:
            current_shard_cooldown = SOUL_SHARD_BASE_COOLDOWN - (self.scythe_stacks * SOUL_SHARD_REDUCTION_PER_STACK)
            if current_time - self.last_shard_time > current_shard_cooldown:
                self.last_shard_time = current_time
                if self.player.game.enemies:
                    target = self.player.game.enemies.sprites()[0]
                    new_shard = SoulShard(self.player.pos, target)
                    self.player.game.player_attack_hitboxes.add(new_shard)
        if self.current_scythe_cooldown < SCYTHE_COOLDOWN:
            self.current_scythe_cooldown += 2
        if self.current_burst_cooldown < SOUL_BURST_COOLDOWN:
            self.current_burst_cooldown += 2

    def start_charge(self):
        if not self.is_charging:
            self.is_charging = True
            self.charge_start_time = pygame.time.get_ticks()
    
    def release_charge(self, player_attack_group):
        current_time = pygame.time.get_ticks()
        if self.is_charging and current_time - self.last_burst_time > self.current_burst_cooldown:
            self.is_charging = False
            self.last_burst_time = current_time
            charge_duration = current_time - self.charge_start_time
            power_ratio = min(charge_duration, self.current_charge_time) / self.current_charge_time
            damage = SOUL_BURST_MIN_DAMAGE + (SOUL_BURST_MAX_DAMAGE - SOUL_BURST_MIN_DAMAGE) * power_ratio
            burst_pos = pygame.mouse.get_pos()
            new_burst = SoulBurst(burst_pos, SOUL_BURST_RADIUS, damage, 300)
            player_attack_group.add(new_burst)
            return True
        self.is_charging = False
        return False

    def on_scythe_hit(self):
        if self.scythe_stacks < MAX_SCYTHE_STACKS:
            self.scythe_stacks += 1
        self.current_charge_time -= SCYTHE_CHARGE_REDUCTION
        if self.current_charge_time < SOUL_BURST_MIN_CHARGE_TIME:
            self.current_charge_time = SOUL_BURST_MIN_CHARGE_TIME
        self.last_scythe_hit_time = pygame.time.get_ticks()

    def activate_skill_2(self, effect_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_scythe_time > self.current_scythe_cooldown:
            self.last_scythe_time = current_time
            mouse_pos = pygame.mouse.get_pos()
            player_pos = self.player.pos
            direction = (pygame.math.Vector2(mouse_pos) - player_pos).normalize()
            scythe_pos = player_pos + direction * 60
            new_scythe = SpectralScythe(scythe_pos, SCYTHE_HITBOX_SIZE, SCYTHE_DURATION, direction)
            effect_group.add(new_scythe)
            return True
        return False

    def reduce_cooldowns(self, skill_number):
        if skill_number == 1:
            self.current_scythe_cooldown -= CAIM_COOLDOWN_REDUCTION
            if self.current_scythe_cooldown < 200: self.current_scythe_cooldown = 200
        elif skill_number == 2:
            self.current_burst_cooldown -= CAIM_COOLDOWN_REDUCTION
            if self.current_burst_cooldown < 200: self.current_burst_cooldown = 200