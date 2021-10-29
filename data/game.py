import pygame
from data import settings


class Game(object):

    def __init__(self, surface):
        self.exit_game = False
        self.clock = pygame.time.Clock()
        self.surface = surface

        self.loop()

    def loop(self):
        while not self.exit_game:
            self.clock.tick(settings.FPS)
            self.handle_events()
            self.run_logic()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    z = pygame.mouse.get_pos()
                if event.button == 2:
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pass
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    pass
                if event.key == pygame.K_F3:
                    pass

    def run_logic(self):
        pass

    def render(self):
        self.surface.fill(settings.COLOR_BLACK)
        pygame.display.flip()
