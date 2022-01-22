import random
import pygame
from src.handler import RESA_CH, RESA_EH, RESA_SSH, RESA_GDH

BROADLEAF = 1
PALM = 2
EVERGREEN = 3


class Tree(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], tree_type: int) -> None:
        """ Initializes a field

        :param position: position on world surface
        :param tree_type: tree type
        """
        pygame.sprite.Sprite.__init__(self)

        # basic settings
        self.growth = random.choice([0, 1, 2])
        self.planted = 0
        self.sprite_id = {}
        if tree_type == BROADLEAF:
            self.sprite_id = {
                0: 0,
                1: 6,
                2: 12
            }
        elif tree_type == PALM:
            self.sprite_id = {
                0: 2,
                1: 8,
                2: 14
            }
        else:
            self.sprite_id = {
                0: 1,
                1: 7,
                2: 13
            }
        self.sprite_sheet_id = 'Trees'
        self.position = position
        self.images = {0: None, 1: None, 2: None}

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

        self.image = self.images[self.growth]

        # positions
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.position

    def update(self, event: pygame.event.Event = None) -> None:
        """ Updates tree by its position

        :param event: optional event
        :return: None
        """
        if event is not None:
            if event.type == RESA_EH.RESA_GAME_EVENT:
                if event.code == RESA_EH.RESA_CTRL_MAP_MOVE:
                    pos_x = self.position[0] + event.move[0]
                    pox_y = self.position[1] + event.move[1]
                    self.position = (pos_x, pox_y)

        # tree growth
        if self.growth < 2:
            hour = RESA_GDH.get_game_time_diff(self.planted, 'h')
            if hour > RESA_CH.tree_growth:
                self.planted = RESA_GDH.game_time
                self.growth += 1
                self.image = self.images[self.growth]

        self.rect.bottomleft = self.position

    def delete(self) -> None:
        """ Deletes the tree

        :return: None
        """
        self.kill()

    def __str__(self):
        return f'Tree - ' \
               f'Pos: {self.position} | ' \
               f'Solid: {self.growth} | '

    def __repr__(self):
        return f'Tree - ' \
               f'Pos: {self.position} | ' \
               f'Solid: {self.growth} | '
