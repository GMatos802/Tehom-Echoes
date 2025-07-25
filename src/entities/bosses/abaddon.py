import pygame
from settings import *


class Abaddon(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((ABADDON_WIDTH, ABADDON_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT * 0.2))
        self.health = 50

        self.player = player
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = ABADDON_SPEED

        self.state = 'chasing'
        self.last_attack_time = 0
        self.action_start_time = 0
        self.attack_direction = pygame.math.Vector2()

    def take_damage(self, amount):
        self.health -= amount
        print(f"Abaddon health: {self.health}")
        if self.health <= 0:
            self.kill()

    def update(self):
        current_time = pygame.time.get_ticks()
        direction_to_player = self.player.pos - self.pos
        distance_to_player = direction_to_player.length()

        if self.state == 'chasing':
            if current_time - self.last_attack_time > ABADDON_ATTACK_COOLDOWN and distance_to_player < ABADDON_ATTACK_RADIUS:
                self.state = 'wind_up'
                self.action_start_time = current_time
                self.attack_direction = direction_to_player.normalize()

        elif self.state == 'wind_up':
            if current_time - self.action_start_time > ABADDON_WINDUP_DURATION:
                self.state = 'attacking'
                self.action_start_time = current_time

        elif self.state == 'attacking':
            if current_time - self.action_start_time > ABADDON_ATTACK_DURATION:
                self.state = 'chasing'
                self.last_attack_time = current_time

        if self.state == 'chasing':
            if distance_to_player > 5:
                self.pos += direction_to_player.normalize() * self.speed
                self.rect.center = self.pos

        elif self.state == 'wind_up':
            # efeito visual no futuro
            pass

        elif self.state == 'attacking':
            self.pos += self.attack_direction * (self.speed * 8)
            self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)
