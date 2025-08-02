import pygame
from settings import *
from ui.hud import HUD
from ui.button import Button
from entities.characters.base_player import Player
from entities.characters.caim import Caim
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
        self.state = 'MAIN_MENU'
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        button_y_start = HEIGHT * 0.4
        self.main_menu_buttons = [
            Button(WIDTH/2 - 150, button_y_start, 300, 50, "Iniciar", self.font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
            Button(WIDTH/2 - 150, button_y_start + 70, 300, 50, "Personagens", self.font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
            Button(WIDTH/2 - 150, button_y_start + 140, 300, 50, "Poderes", self.font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
            Button(WIDTH/2 - 150, button_y_start + 210, 300, 50, "Chefes", self.font, BUTTON_COLOR, BUTTON_HOVER_COLOR),
            Button(WIDTH/2 - 150, button_y_start + 280, 300, 50, "Sair", self.font, BUTTON_COLOR, BUTTON_HOVER_COLOR)
        ]
        
        self.end_screen_button = Button(
            WIDTH/2 - 150, HEIGHT * 0.6, 300, 50, 
            "Voltar ao Menu", self.font, BUTTON_COLOR, BUTTON_HOVER_COLOR
        )

        self.chosen_character = None
        self.player = None
        self.hud = None
        self.projectiles = None
        self.effects = None
        self.enemies = None
        self.attack_hitboxes = None
        self.player_attack_hitboxes = None
        self.enemy_projectiles = None

    def start_new_game(self, kit_class):
        self.player = self.chosen_character(self, kit_class)
        self.projectiles = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.attack_hitboxes = pygame.sprite.Group()
        self.player_attack_hitboxes = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        abaddon = Abaddon(self.player, self.attack_hitboxes, self.enemy_projectiles)
        self.enemies.add(abaddon)
        self.hud = HUD(self.player, self.enemies)

    def run(self):
        while self.running:
            if self.state == 'MAIN_MENU':
                self.run_main_menu()
            elif self.state == 'CHARACTER_SELECTION':
                self.run_character_selection()
            elif self.state == 'KIT_SELECTION':
                self.run_kit_selection()
            elif self.state == 'CHARACTERS_SCREEN':
                self.run_characters_screen()
            elif self.state == 'POWERS_SCREEN':
                self.run_powers_screen()
            elif self.state == 'BOSSES_SCREEN':
                self.run_bosses_screen()
            elif self.state == 'PLAYING':
                self.run_gameplay()
            elif self.state == 'GAME_OVER':
                self.run_game_over_screen()
            elif self.state == 'VICTORY':
                self.run_victory_screen() 
        pygame.quit()

    def run_main_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill(BLACK)
        
        title_surface = self.font.render("Tehom Echoes", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.2))
        self.screen.blit(title_surface, title_rect)

        for button in self.main_menu_buttons:
            button.check_for_hover(mouse_pos)
            button.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.main_menu_buttons[0].is_clicked(event):
                self.state = 'CHARACTER_SELECTION'
            if self.main_menu_buttons[1].is_clicked(event):
                self.state = 'CHARACTERS_SCREEN'
            if self.main_menu_buttons[2].is_clicked(event):
                self.state = 'POWERS_SCREEN'
            if self.main_menu_buttons[3].is_clicked(event):
                self.state = 'BOSSES_SCREEN'
            if self.main_menu_buttons[4].is_clicked(event):
                self.running = False
        
        pygame.display.flip()

    def run_character_selection(self):
        self.screen.fill(BLACK)

        title_surface = self.font.render("Escolha seu Personagem", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.3))
        self.screen.blit(title_surface, title_rect)
        
        option_caim = self.font.render("Pressione [1] para CAIM", True, WHITE)
        option_caim_rect = option_caim.get_rect(center=(WIDTH / 2, HEIGHT * 0.5))
        self.screen.blit(option_caim, option_caim_rect)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.chosen_character = Caim
                    self.state = 'KIT_SELECTION'

    def run_kit_selection(self):
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

    def run_characters_screen(self):
        self.screen.fill(BLACK)
        
        def draw_text(text, y_pos, font, color):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH / 2, y_pos))
            self.screen.blit(text_surface, text_rect)

        draw_text("Personagens", HEIGHT * 0.1, self.font, WHITE)
        draw_text("Caim, o Primeiro Andarilho", HEIGHT * 0.3, self.small_font, WHITE)
        draw_text("- Passiva: Dano aumenta com base na vida perdida.", HEIGHT * 0.35, self.small_font, (200,200,200))
        draw_text("- Passiva: Ataques custam vida e reduzem cooldown se bem sucedidos", HEIGHT * 0.4, self.small_font, (200,200,200))
        draw_text("Pressione ESC para voltar", HEIGHT * 0.9, self.small_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'MAIN_MENU'
        
        pygame.display.flip()

    def run_powers_screen(self):
        self.screen.fill(BLACK)
        
        def draw_text(text, y_pos, font, color):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH / 2, y_pos))
            self.screen.blit(text_surface, text_rect)

        draw_text("Descrição dos Poderes", HEIGHT * 0.1, self.font, WHITE)
        draw_text("[LUZ]: Foco em ataques a distancia e precisao.", HEIGHT * 0.3, self.small_font, YELLOW)
        draw_text("[FURIA]: Foco em combate corpo a corpo agressivo e combos.", HEIGHT * 0.4, self.small_font, RED)
        draw_text("[ALMA]: Foco em ataques carregados e sinergia entre habilidades.", HEIGHT * 0.5, self.small_font, BLUE)
        draw_text("Pressione ESC para voltar", HEIGHT * 0.9, self.small_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'MAIN_MENU'
        
        pygame.display.flip()

    def run_bosses_screen(self):
        self.screen.fill(BLACK)
        
        def draw_text(text, y_pos, font, color):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH / 2, y_pos))
            self.screen.blit(text_surface, text_rect)
            
        draw_text("Bestiário Infernal", HEIGHT * 0.1, self.font, WHITE)
        draw_text("Abaddon, o Destruidor: Mestre da forca bruta e ataques em area.", HEIGHT * 0.3, self.small_font, WHITE)
        draw_text("Pressione ESC para voltar", HEIGHT * 0.9, self.small_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'MAIN_MENU'
        
        pygame.display.flip()

    def run_game_over_screen(self):
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        title_surface = self.font.render("VOCE MORREU", True, RED)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.4))
        self.screen.blit(title_surface, title_rect)

        self.end_screen_button.check_for_hover(mouse_pos)
        self.end_screen_button.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.end_screen_button.is_clicked(event):
                self.state = 'MAIN_MENU' 
        
        pygame.display.flip()

    def run_victory_screen(self):
        self.screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        title_surface = self.font.render("VITORIA", True, YELLOW)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT * 0.4))
        self.screen.blit(title_surface, title_rect)

        self.end_screen_button.check_for_hover(mouse_pos)
        self.end_screen_button.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.end_screen_button.is_clicked(event):
                self.state = 'MAIN_MENU' 
        
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
                    else:
                        self.player.use_skill_1(self.player_attack_hitboxes)
                if event.button == 3:
                    if isinstance(self.player.kit, (LightKit, SoulKit)):
                        self.player.use_skill_2(self.effects)
                    elif isinstance(self.player.kit, FuryKit):
                        self.player.use_skill_2(self.player_attack_hitboxes)

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

        if not self.enemies:
            self.state = 'VICTORY'
            return 

        all_player_attacks = pygame.sprite.Group(self.player_attack_hitboxes, self.effects)
        player_attacks_hit = pygame.sprite.groupcollide(
            all_player_attacks, self.enemies, False, False)

        for hitbox, enemies_hit in player_attacks_hit.items():
            for enemy in enemies_hit:
                if enemy not in hitbox.enemies_hit:
                    if isinstance(hitbox, (Slash, RushHitbox)):
                        damage_dealt = SLASH_DAMAGE * self.player.get_damage_multiplier()
                        enemy.take_damage(damage_dealt)
                        if hasattr(self.player.kit, 'on_slash_hit'):
                            self.player.kit.on_slash_hit()
                        self.player.gain_health(HEALTH_REGEN_ON_SLASH_HIT)
                    elif isinstance(hitbox, HolySpear):
                        damage_dealt = 1 * self.player.get_damage_multiplier()
                        enemy.take_damage(damage_dealt)
                        if hasattr(self.player.kit, 'on_spear_hit'):
                            self.player.kit.on_spear_hit()
                        self.player.gain_health(HEALTH_REGEN_ON_SPEAR_HIT)
                        hitbox.kill()
                    elif isinstance(hitbox, SpectralScythe):
                        damage_dealt = SCYTHE_DAMAGE * self.player.get_damage_multiplier()
                        enemy.take_damage(damage_dealt)
                        if hasattr(self.player.kit, 'on_scythe_hit'):
                            self.player.kit.on_scythe_hit()
                        self.player.gain_health(HEALTH_REGEN_ON_SOUL_HIT)
                    elif isinstance(hitbox, SoulBurst):
                        damage_dealt = hitbox.damage * self.player.get_damage_multiplier()
                        enemy.take_damage(damage_dealt)
                        healing_amount = damage_dealt * SOUL_BURST_LIFESTEAL_RATIO
                        self.player.gain_health(healing_amount)
                    elif isinstance(hitbox, SoulShard):
                        damage_dealt = SOUL_SHARD_DAMAGE * self.player.get_damage_multiplier()
                        enemy.take_damage(damage_dealt)
                        self.player.gain_health(HEALTH_REGEN_ON_SHARD_HIT)
                        hitbox.kill()
                    elif isinstance(hitbox, LuminousPulse):
                        damage_dealt = PULSE_DAMAGE * self.player.get_damage_multiplier()
                        enemy.take_damage(damage_dealt)
                        self.player.gain_health(HEALTH_REGEN_ON_PULSE_HIT)
                    
                    self.player.on_ability_hit(hitbox)
                    hitbox.enemies_hit.append(enemy)

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