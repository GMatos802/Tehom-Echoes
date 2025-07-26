import pygame
from settings import *
import random
from entities.enemy_projectiles import Shockwave, HomingSwarm


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
        self.max_health = 50

        self.player = player
        self.attack_hitboxes = attack_hitbox_group
        self.enemy_projectiles = enemy_projectile_group
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = ABADDON_SPEED

        self.is_hit = False
        self.hit_time = 0
        self.in_phase_2 = False

        self.state = 'chasing'
        self.last_attack_time = 0
        self.action_start_time = 0
        self.attack_direction = pygame.math.Vector2()
        self.last_swarm_time = 0
        self.last_charge_shot_time = 0

    def take_damage(self, amount):
        if not self.is_hit:
            self.health -= amount
            print(f"Abaddon health: {self.health}")

            if self.health <= (self.max_health / 2) and not self.in_phase_2:
                self.in_phase_2 = True
                print("ABADDON ENTROU NA FASE 2!")

            if self.health <= 0:
                self.kill()

            self.is_hit = True
            self.hit_time = pygame.time.get_ticks()
            self.image.fill(WHITE)

    def update(self):
        # Gerenciador de Cor e Flash
        if self.is_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > HIT_FLASH_DURATION:
                self.is_hit = False
                if self.in_phase_2:
                    self.image.fill((150, 0, 0)) # Vermelho escuro da Fase 2
                else:
                    self.image.fill(RED) # Vermelho normal da Fase 1

        current_time = pygame.time.get_ticks()

        if self.in_phase_2 and current_time - self.last_swarm_time > SWARM_COOLDOWN:
            for i in range(3):
                new_swarm_projectile = HomingSwarm(self.pos, self.player)
                self.enemy_projectiles.add(new_swarm_projectile)
            self.last_swarm_time = current_time

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
                    self.attack_direction = direction_to_player.normalize()
                    # Aprimoramento da Fase 2: Sempre usa o golpe em arco de perto
                    self.state = 'swinging'
                    if self.in_phase_2:
                        # Adiciona a Onda de Ruína ao golpe
                        new_shockwave = Shockwave(self.pos, self.attack_direction)
                        self.enemy_projectiles.add(new_shockwave)
                    
                    hitbox_pos = self.pos + self.attack_direction * 75
                    hitbox_size = (SWING_HITBOX_WIDTH, SWING_HITBOX_HEIGHT)
                    swing_attack = HitboxSprite(hitbox_pos, hitbox_size, 500)
                    self.attack_hitboxes.add(swing_attack)
                    self.action_start_time = current_time
                    self.last_attack_time = current_time

                # Se o jogador está LONGE (zona de gap close / ataque à distância)...
                elif distance_to_player < ABADDON_CHARGE_RADIUS:
                    self.attack_direction = direction_to_player.normalize()
                    choice = random.choice(['charge', 'shockwave'])

                    if choice == 'charge':
                        self.state = 'wind_up'
                    else:  # 'shockwave'
                        new_shockwave = Shockwave(self.pos, self.attack_direction)
                        self.enemy_projectiles.add(new_shockwave)
                        self.last_attack_time = current_time

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
            # Aprimoramento da Fase 2
            if self.in_phase_2:
                if current_time - self.last_charge_shot_time > CHARGE_SHOT_COOLDOWN:
                    left_direction = self.attack_direction.rotate(90)
                    right_direction = self.attack_direction.rotate(-90)
                    self.enemy_projectiles.add(Shockwave(self.pos, left_direction))
                    self.enemy_projectiles.add(Shockwave(self.pos, right_direction))
                    self.last_charge_shot_time = current_time
            
            if current_time - self.action_start_time > ABADDON_ATTACK_DURATION:
                self.state = 'chasing'

        elif self.state == 'swinging':
            if current_time - self.action_start_time > 500:
                self.state = 'chasing'

    def draw(self, surface):
        surface.blit(self.image, self.rect)
