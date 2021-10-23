import pygame
pygame.init()


class Game(object):

    def __init__(self):
        self.game_running = False
        self.exit_game = False
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((1280, 800))

        pygame.display.set_caption("Resa")

        self.loop()

    def loop(self):
        while not self.exit_game:
            self.clock.tick(self.fps)
            self.handle_events()
            self.run_logic()
            self.render()

        self.exit()

    def handle_events(self):
        if not self.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_F3:
                        print("[INFO] debugging")
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True
                    print("[INFO] bye")

    def run_logic(self):
        pass

    def render(self):
        self.surface.fill((0, 0, 111))
        pygame.display.flip()

    @staticmethod
    def exit():
        pygame.quit()
