import pygame
from settings import *
from entities.player import Player
from entities.dummy_enemy import DummyEnemy
from powers.kits import LightKit


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # self.game_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(self)
        self.projectiles = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        dummy = DummyEnemy((WIDTH * 0.75, HEIGHT // 2))
        self.enemies.add(dummy)

    def run(self):
        while self.running:

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.kit.activate_skill_1(self.projectiles)
                    if event.button == 3:
                        self.player.kit.activate_skill_2(self.effects)

            self.player.update()
            self.projectiles.update()
            self.effects.update()

            collisions = pygame.sprite.groupcollide(
                self.projectiles, self.enemies, True, False)
            for projectile, enemies_hit in collisions.items():
                for enemy in enemies_hit:
                    enemy.take_damage(1)

            pulse_collisions = pygame.sprite.groupcollide(
                self.effects, self.enemies, False, False)
            for effect, enemies_hit in pulse_collisions.items():
                for enemy in enemies_hit:
                    if enemy not in effect.enemies_hit:
                        enemy.take_damage(PULSE_DAMAGE)
                        effect.enemies_hit.append(enemy)

            # pygame.sprite.groupcollide(self.effects, self.enemy_projectiles, False, True)

            self.screen.fill(BLACK)

            self.player.draw(self.screen)
            self.projectiles.draw(self.screen)
            self.effects.draw(self.screen)
            self.enemies.draw(self.screen)

            # scaled_surface = pygame.transform.scale(
            # self.game_surface, (WIDTH, HEIGHT))
            # self.screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()

        pygame.quit()
