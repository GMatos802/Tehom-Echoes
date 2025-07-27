import pygame
from settings import *
from ui.hud import HUD
from entities.player import Player
from entities.bosses.abaddon import Abaddon
from powers.kits import LightKit, FuryKit


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(self)
        self.hud = HUD(self.player)
        self.projectiles = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.attack_hitboxes = pygame.sprite.Group()
        self.player_attack_hitboxes = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()

        abaddon = Abaddon(self.player, self.attack_hitboxes, self.enemy_projectiles)
        self.enemies.add(abaddon)

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if hasattr(self.player.kit, 'activate_skill_1'):
                            self.player.kit.activate_skill_1(self.player_attack_hitboxes)

                    if event.button == 3:
                        if hasattr(self.player.kit, 'activate_skill_2'):
                            if isinstance(self.player.kit, FuryKit):
                                self.player.kit.activate_skill_2(self.player_attack_hitboxes)
                            elif isinstance(self.player.kit, LightKit):
                                self.player.kit.activate_skill_2(self.effects)

            self.player.update()
            self.projectiles.update()
            self.effects.update()
            self.enemies.update()
            self.enemy_projectiles.update()
            self.attack_hitboxes.update()
            self.player_attack_hitboxes.update()

            player_attacks_hit = pygame.sprite.groupcollide(
                self.player_attack_hitboxes, self.enemies, False, False)
            for hitbox, enemies_hit in player_attacks_hit.items():
                for enemy in enemies_hit:
                    if enemy not in hitbox.enemies_hit:
                        enemy.take_damage(SLASH_DAMAGE) 
                        if hasattr(self.player.kit, 'on_slash_hit'):
                            self.player.kit.on_slash_hit()
                        self.player.gain_health(2 )

                        hitbox.enemies_hit.append(enemy)

            pulse_collisions = pygame.sprite.groupcollide(
                self.effects, self.enemies, False, False)
            for effect, enemies_hit in pulse_collisions.items():
                for enemy in enemies_hit:
                    if enemy not in effect.enemies_hit:
                        enemy.take_damage(PULSE_DAMAGE)
                        effect.enemies_hit.append(enemy)
                        self.player.gain_health(HEALTH_REGEN_ON_PULSE_HIT)

            enemy_projectile_hits = pygame.sprite.spritecollide(
                self.player, self.enemy_projectiles, True)
            if enemy_projectile_hits:
                self.player.take_damage(15)

            player_hit_by_touch = pygame.sprite.spritecollide(
                self.player, self.enemies, False)
            if player_hit_by_touch:
                self.player.take_damage(10)

            player_hit_by_swing = pygame.sprite.spritecollide(
                self.player, self.attack_hitboxes, False)
            if player_hit_by_swing:
                self.player.take_damage(25)

            pygame.sprite.groupcollide(
                self.effects, self.enemy_projectiles, False, True)

            self.screen.fill(BLACK)

            self.enemies.draw(self.screen)
            self.effects.draw(self.screen)
            self.projectiles.draw(self.screen)
            self.attack_hitboxes.draw(self.screen)
            self.enemy_projectiles.draw(self.screen)
            self.player.draw(self.screen)
            self.hud.draw(self.screen)
            self.player_attack_hitboxes.draw(self.screen)

            pygame.display.flip()

        pygame.quit()