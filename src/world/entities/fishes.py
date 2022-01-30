import pygame
from src.handler import RESA_CH, RESA_EH, RESA_SSH


class Fishes(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]) -> None:
        pygame.sprite.Sprite.__init__(self)

        # basic settings
        self.speed = 5
        self.speed_state = 0
        self.sprite_id = 0
        self.sprite_sheet_id = 'Fishes'
        self.position = position
        self.images = {}

        # image and sprite settings
        self.image = RESA_SSH.image_by_index(self.sprite_sheet_id, 0)
        self.size = RESA_SSH.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2)
        self.images[0] = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.image = RESA_SSH.image_by_index(self.sprite_sheet_id, 1)
        self.size = RESA_SSH.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2)
        self.images[1] = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.image = RESA_SSH.image_by_index(self.sprite_sheet_id, 2)
        self.size = RESA_SSH.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2)
        self.images[2] = pygame.transform.scale(self.image, self.size).convert_alpha()

        self.animate()

        # positions
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.position

    def animate(self):
        if self.sprite_id == 2:
            self.sprite_id = 0
        else:
            self.sprite_id += 1

        self.image = self.images[self.sprite_id]

    def update(self, event: pygame.event.Event = None) -> None:
        if event is not None:
            if event.type == RESA_EH.GAME_EVENT:
                if event.code == RESA_EH.CTRL_MAP_MOVE:
                    pos_x = self.position[0] + event.move[0]
                    pox_y = self.position[1] + event.move[1]
                    self.position = (pos_x, pox_y)
        else:
            if self.speed_state == self.speed:
                self.animate()
                self.speed_state = 0
            else:
                self.speed_state += 1

        self.rect.bottomleft = self.position

    def delete(self) -> None:
        self.kill()
