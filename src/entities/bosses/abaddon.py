import pygame
from settings import *
import random
from entities.enemy_projectiles import Shockwave


class HitboxSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, duration):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 128))
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()


class Abaddon(pygame.sprite.Sprite):
    def __init__(self, player, attack_hitbox_group, enemy_projectile_group):
        super().__init__()
        self.image = pygame.Surface((ABADDON_WIDTH, ABADDON_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT * 0.2))
        self.health = 50

        self.player = player
        self.attack_hitboxes = attack_hitbox_group
        self.enemy_projectiles = enemy_projectile_group
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = ABADDON_SPEED

        self.is_hit = False
        self.hit_time = 0

        self.state = 'chasing'
        self.last_attack_time = 0
        self.action_start_time = 0
        self.attack_direction = pygame.math.Vector2()

    def take_damage(self, amount):
        if not self.is_hit:
            self.health -= amount
            print(f"Abaddon health: {self.health}")
            if self.health <= 0:
                self.kill()

            self.is_hit = True
            self.hit_time = pygame.time.get_ticks()
            self.image.fill(WHITE)

    def update(self):
        if self.is_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.is_hit > HIT_FLASH_DURATION:
                self.is_hit = False
                self.image.fill(RED)

        current_time = pygame.time.get_ticks()
        direction_to_player = self.player.pos - self.pos
        distance_to_player = 0
        if direction_to_player.length() > 0:
            distance_to_player = direction_to_player.length()

        # --- MÁQUINA DE ESTADOS REFINADA ---

        if self.state == 'chasing':
            # AÇÃO: Perseguir o jogador
            if distance_to_player > 5:
                self.pos += direction_to_player.normalize() * self.speed
                self.rect.center = self.pos

            # TRANSIÇÃO: Checar se pode atacar
            if current_time - self.last_attack_time > ABADDON_ATTACK_COOLDOWN:
                # Se o jogador está PERTO (zona de combate corpo a corpo)...
                if distance_to_player < ABADDON_ATTACK_RADIUS:
                    # ... a prioridade é o ataque em arco.
                    self.attack_direction = direction_to_player.normalize()
                    self.state = 'swinging'
                    hitbox_pos = self.pos + self.attack_direction * 75
                    hitbox_size = (SWING_HITBOX_WIDTH, SWING_HITBOX_HEIGHT)
                    swing_attack = HitboxSprite(hitbox_pos, hitbox_size, 500)
                    self.attack_hitboxes.add(swing_attack)
                    self.action_start_time = current_time
                    self.last_attack_time = current_time

                # Se o jogador está LONGE (zona de gap close / ataque à distância)...
                elif distance_to_player < ABADDON_CHARGE_RADIUS:
                    # ... ele escolhe entre a investida (para se aproximar) ou a onda (para pressionar).
                    self.attack_direction = direction_to_player.normalize()
                    choice = random.choice(['charge', 'shockwave'])

                    if choice == 'charge':
                        self.state = 'wind_up'
                    else:  # 'shockwave'
                        new_shockwave = Shockwave(
                            self.pos, self.attack_direction)
                        self.enemy_projectiles.add(new_shockwave)
                        # Reseta o cooldown, mas continua perseguindo
                        self.last_attack_time = current_time

                    # Apenas a investida precisa de um timer de ação
                    if self.state == 'wind_up':
                        self.action_start_time = current_time
                        self.last_attack_time = current_time

        elif self.state == 'wind_up':
            if current_time - self.action_start_time > ABADDON_WINDUP_DURATION:
                self.state = 'attacking'
                self.action_start_time = current_time

        elif self.state == 'attacking':
            self.pos += self.attack_direction * (self.speed * 8)
            self.rect.center = self.pos
            if current_time - self.action_start_time > ABADDON_ATTACK_DURATION:
                self.state = 'chasing'

        elif self.state == 'swinging':
            if current_time - self.action_start_time > 500:
                self.state = 'chasing'

    def draw(self, surface):
        surface.blit(self.image, self.rect)
