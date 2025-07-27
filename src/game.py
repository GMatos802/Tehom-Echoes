import pygame
from settings import *
from ui.hud import HUD
from entities.player import Player
from entities.bosses.abaddon import Abaddon
from powers.kits import LightKit, FuryKit, SoulKit
from powers.skills.light_skills import HolySpear, LuminousPulse
from powers.skills.fury_skills import Slash, RushHitbox
from powers.skills.soul_skills import SpectralScythe, SoulBurst, SoulShard

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'START_SCREEN'
        self.font = pygame.font.Font(None, 48)

        self.player = None
        self.hud = None
        self.projectiles = None
        self.effects = None
        self.enemies = None
        self.attack_hitboxes = None
        self.player_attack_hitboxes = None
        self.enemy_projectiles = None

    def start_new_game(self, kit_class):
        self.player = Player(self, kit_class)
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
            if self.state == 'START_SCREEN':
                self.run_start_screen()
            elif self.state == 'PLAYING':
                self.run_gameplay()
        
        pygame.quit()

    def run_start_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.start_new_game(LightKit)
                    self.state = 'PLAYING' 
                if event.key == pygame.K_2:
                    self.start_new_game(FuryKit)
                    self.state = 'PLAYING' 
                if event.key == pygame.K_3:
                    self.start_new_game(SoulKit)
                    self.state = 'PLAYING'

        self.screen.fill(BLACK)

        title_surface = self.font.render("Escolha seu Kit Inicial", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.3))

        option1_surface = self.font.render("Pressione [1] para LUZ", True, YELLOW)
        option1_rect = option1_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.5))

        option2_surface = self.font.render("Pressione [2] para FURIA", True, RED)
        option2_rect = option2_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.6))

        option3_surface = self.font.render("Pressione [3] para ALMA", True, BLUE)
        option3_rect = option3_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.7))

        self.screen.blit(title_surface, title_rect)
        self.screen.blit(option1_surface, option1_rect)
        self.screen.blit(option2_surface, option2_rect)
        self.screen.blit(option3_surface, option3_rect)

        pygame.display.flip()

    def run_gameplay(self):
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if isinstance(self.player.kit, SoulKit):
                        self.player.kit.start_charge()
                    elif hasattr(self.player.kit, 'activate_skill_1'):
                        self.player.kit.activate_skill_1(self.player_attack_hitboxes)
                if event.button == 3:
                    if hasattr(self.player.kit, 'activate_skill_2'):
                        if isinstance(self.player.kit, (LightKit, SoulKit)):
                            self.player.kit.activate_skill_2(self.effects)
                        elif isinstance(self.player.kit, FuryKit):
                            self.player.kit.activate_skill_2(self.player_attack_hitboxes)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    if isinstance(self.player.kit, SoulKit):
                        self.player.kit.release_charge(self.player_attack_hitboxes)
        
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
                    if isinstance(hitbox, (Slash, RushHitbox)):
                        enemy.take_damage(SLASH_DAMAGE)
                        if hasattr(self.player.kit, 'on_slash_hit'):
                            self.player.kit.on_slash_hit()
                        self.player.gain_health(HEALTH_REGEN_ON_SLASH_HIT)
                    elif isinstance(hitbox, HolySpear):
                        enemy.take_damage(1)
                        if hasattr(self.player.kit, 'on_spear_hit'):
                            self.player.kit.on_spear_hit()
                        self.player.gain_health(HEALTH_REGEN_ON_SPEAR_HIT)
                    elif isinstance(hitbox, SoulBurst):
                        enemy.take_damage(hitbox.damage)
                        healing_amount = hitbox.damage * SOUL_BURST_LIFESTEAL_RATIO
                        self.player.gain_health(healing_amount)

                    elif isinstance(hitbox, SoulShard):
                        enemy.take_damage(SOUL_SHARD_DAMAGE)
                        self.player.gain_health(HEALTH_REGEN_ON_SHARD_HIT)
                        hitbox.kill()
                    
                    hitbox.enemies_hit.append(enemy)

        effects_hit = pygame.sprite.groupcollide(
            self.effects, self.enemies, False, False)
        for effect, enemies_hit in effects_hit.items():
            for enemy in enemies_hit:
                if enemy not in effect.enemies_hit:
                    if isinstance(effect, LuminousPulse):
                        enemy.take_damage(PULSE_DAMAGE)
                        self.player.gain_health(HEALTH_REGEN_ON_PULSE_HIT)
                    elif isinstance(effect, SpectralScythe):
                        enemy.take_damage(SCYTHE_DAMAGE)
                        if hasattr(self.player.kit, 'on_scythe_hit'):
                            self.player.kit.on_scythe_hit()
                        self.player.gain_health(HEALTH_REGEN_ON_SOUL_HIT)
                    
                    effect.enemies_hit.append(enemy)

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