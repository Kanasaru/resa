import pygame
from src.handler import RESA_CH, RESA_EH, RESA_SSH


class Wheat(object):
    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.images = {0: None, 1: None, 2: None, 3: None}
        self.sprite_id = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
        }
        self.sprite_sheet_id = 'Farmfields'
        self.growth = 0
        self.grow_speed = 24
        self.grow_factor = 1.0
        self.planted = 0

        # image and sprite settings
        self.image = RESA_SSH.image_by_index(self.sprite_sheet_id, self.sprite_id[0])
        self.size = RESA_SSH.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2)
        self.images[0] = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.image = RESA_SSH.image_by_index(self.sprite_sheet_id, self.sprite_id[1])
        self.size = RESA_SSH.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2)
        self.images[1] = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.image = RESA_SSH.image_by_index(self.sprite_sheet_id, self.sprite_id[2])
        self.size = RESA_SSH.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2)
        self.images[2] = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.image = RESA_SSH.image_by_index(self.sprite_sheet_id, self.sprite_id[3])
        self.size = RESA_SSH.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2)
        self.images[3] = pygame.transform.scale(self.image, self.size).convert_alpha()

        self.image = self.images[self.growth]

        # positions
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.position

    def update(self, event: pygame.event.Event = None) -> None:
        if event is not None:
            if event.type == RESA_EH.GAME_EVENT:
                if event.code == RESA_EH.CTRL_MAP_MOVE:
                    pos_x = self.position[0] + event.move[0]
                    pox_y = self.position[1] + event.move[1]
                    self.position = (pos_x, pox_y)
            if event.type == RESA_EH.GAME_CLOCK:
                if self.growth < 3:
                    if self.planted >= self.grow_speed * self.grow_factor:
                        self.planted = 0
                        self.growth += 1
                        self.image = self.images[self.growth]
                    else:
                        self.planted += 1

        self.rect.bottomleft = self.position
