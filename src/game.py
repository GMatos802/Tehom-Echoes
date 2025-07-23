import pygame
from settings import *
from entities.player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # self.game_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player()

    def run(self):
        while self.running:

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.player.update()

            self.screen.fill(BLACK)

            self.player.draw(self.screen)

            # scaled_surface = pygame.transform.scale(
            # self.game_surface, (WIDTH, HEIGHT))
            # self.screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()
        pygame.quit()
