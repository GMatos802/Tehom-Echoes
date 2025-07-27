import pygame
from settings import *
from powers.kits import LightKit, FuryKit

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT * 0.8))

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.last_move_direction = pygame.math.Vector2(1, 0)

        self.is_dashing = False
        self.dash_end_time = 0
        self.last_dash_time = 0
        self.dash_direction = pygame.math.Vector2()

        self.kit = FuryKit(self)

        self.max_health = PLAYER_MAX_HEALTH
        self.health = PLAYER_MAX_HEALTH
        self.last_hit_time = 0
        self.is_invincible = False

    def get_input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        
        if keys[pygame.K_SPACE]:
            self.start_dash()

    def start_dash(self):
        current_time = pygame.time.get_ticks()
        is_rushing = hasattr(self.kit, 'is_rushing') and self.kit.is_rushing
        if not self.is_dashing and not is_rushing and current_time - self.last_dash_time > DASH_COOLDOWN:
            self.is_dashing = True
            
            if self.direction.length() > 0:
                self.dash_direction = self.direction.normalize()
            else:
                self.dash_direction = self.last_move_direction.normalize()
            
            self.dash_end_time = current_time + DASH_DURATION
            self.last_dash_time = current_time

    def take_damage(self, amount):
        if not self.is_invincible:
            self.health -= amount
            if self.health < 0:
                self.health = 0
            
            self.is_invincible = True
            self.last_hit_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.kill()
                self.game.running = False

    def gain_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def update(self):
        current_time = pygame.time.get_ticks()

        self.health -= HEALTH_DRAIN_RATE
        if self.health <= 0:
            self.kill()
            self.game.running = False
            return 
        
        is_rushing = hasattr(self.kit, 'is_rushing') and self.kit.is_rushing

        if is_rushing:
            self.image.fill(DARK_RED)
            self.image.set_alpha(255)
            self.is_invincible = True
        elif self.is_invincible:
            if current_time - self.last_hit_time > PLAYER_INVINCIBILITY_DURATION:
                self.is_invincible = False
            
            alpha = 255 if int(current_time / 50) % 2 == 0 else 0
            self.image.set_alpha(alpha)
        else:
            self.image.fill(WHITE)
            self.image.set_alpha(255)

        if is_rushing:
            if current_time < self.kit.rush_end_time:
                self.pos += self.kit.rush_direction * PLAYER_SPEED * RUSH_SPEED_MULTIPLIER
            else:
                self.kit.is_rushing = False
        
        elif self.is_dashing:
            if current_time < self.dash_end_time:
                self.pos += self.dash_direction * PLAYER_SPEED * DASH_SPEED_MULTIPLIER
            else:
                self.is_dashing = False
        
        else:
            self.get_input()
            if self.direction.length() > 0:
                self.last_move_direction = self.direction.copy()
                self.pos += self.direction.normalize() * PLAYER_SPEED

        self.rect.center = self.pos
        if hasattr(self.kit, 'update'):
            self.kit.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
