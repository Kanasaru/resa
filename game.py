from grid import Grid
import pygame
pygame.init()


class Game(object):

    def __init__(self):
        self.grid = Grid()
        self.title = "Resa"
        self.version = "0.1.0"
        self.author = "Kanasaru"
        self.resolution = (1280, 800)
        self.exit_game = False
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(self.resolution)

        pygame.display.set_caption(f"{self.title} in version {self.version} by {self.author}")

        self.loop()

    def loop(self):
        while not self.exit_game:
            self.clock.tick(self.fps)
            self.handle_events()
            self.run_logic()
            self.render()

        self.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    z = pygame.mouse.get_pos()
                    if z:
                        print(self.grid.get_field_nr(z))
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
        self.surface.fill((255, 255, 255))
        pos_x = 0
        pos_y = 0
        xy = self.grid.get_grid_size()
        f = self.grid.get_field_size()
        for p in range(xy[1]):
            for i in range(xy[0]):
                pygame.draw.rect(self.surface, (0, 0, 0), (pos_x, pos_y, f, f))
                pos_x += f
            pos_y += f
            pos_x = 0
        test = self.grid.get_field_by_number(23)
        pygame.draw.rect(self.surface, (0, 255, 111), (test[0], test[1], f, f))

        pygame.display.flip()

    def exit(self):
        pygame.quit()
