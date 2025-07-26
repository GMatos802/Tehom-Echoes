import pygame
from settings import *
from ui.hud import HUD
from entities.player import Player
from entities.bosses.abaddon import Abaddon
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
        self.hud = HUD(self.player)
        self.projectiles = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.attack_hitboxes = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()

        abaddon = Abaddon(self.player, self.attack_hitboxes,
                          self.enemy_projectiles)
        self.enemies.add(abaddon)

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
            self.enemies.update()
            self.enemy_projectiles.update()
            self.attack_hitboxes.update()

            collisions = pygame.sprite.groupcollide(
                self.projectiles, self.enemies, True, False)
            for projectile, enemies_hit in collisions.items():
                for enemy in enemies_hit:
                    enemy.take_damage(1)
                    self.player.gain_health(HEALTH_REGEN_ON_SPEAR_HIT)
                    self.player.kit.on_spear_hit()

            pulse_collisions = pygame.sprite.groupcollide(
                self.effects, self.enemies, False, False)
            for effect, enemies_hit in pulse_collisions.items():
                for enemy in enemies_hit:
                    if enemy not in effect.enemies_hit:
                        enemy.take_damage(PULSE_DAMAGE)
                        effect.enemies_hit.append(enemy)
                        self.player.gain_health(HEALTH_REGEN_ON_PULSE_HIT)

            enemy_projectile_hits = pygame.sprite.spritecollide(
                self.player, self.enemy_projectiles, False)
            if enemy_projectile_hits:
                self.player.take_damage(15)

            player_hit = pygame.sprite.spritecollide(
                self.player, self.enemies, False)
            if player_hit:
                self.player.take_damage(10)

            swing_hits = pygame.sprite.spritecollide(
                self.player, self.attack_hitboxes, False)
            if swing_hits:
                self.player.take_damage(25)

            pygame.sprite.groupcollide(
                self.effects, self.enemy_projectiles, False, True)

            # pygame.sprite.groupcollide(self.effects, self.enemy_projectiles, False, True)

            self.screen.fill(BLACK)

            self.enemies.draw(self.screen)
            self.effects.draw(self.screen)
            self.projectiles.draw(self.screen)
            self.attack_hitboxes.draw(self.screen)
            self.enemy_projectiles.draw(self.screen)
            self.player.draw(self.screen)
            self.hud.draw(self.screen)

            # scaled_surface = pygame.transform.scale(
            # self.game_surface, (WIDTH, HEIGHT))
            # self.screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()

        pygame.quit()
