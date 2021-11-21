""" This module provides Field class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.0'

import pygame


class Field(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], image: pygame.image) -> None:
        """ Initializes a field

        :param position: position on world surface
        :param size: field size
        :param image: field image
        """
        pygame.sprite.Sprite.__init__(self)

        self.pos = position
        self.image = image
        self.size = size

        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        self.solid = False
        self.sprite_sheet_id = None
        self.sprite_id = None

    def update(self) -> None:
        """ Updates field by its position

        :return: None
        """
        self.rect.topleft = self.pos

    def set_solid(self, value: bool):
        """ Sets the field attribute 'solid'

        :param value: true or false
        :return: None
        """
        self.solid = value

    def position(self, position: tuple[int, int] = None) -> tuple | bool:
        """ Sets the position of the field or returns its current position

        :param position: position that should be set
        :return: true if given position was set as new position or current position if no position is given
        """
        if position is not None:
            self.pos = position
            return True
        return int(self.pos[0]), int(self.pos[1])

    def move(self, movement: tuple[int, int]) -> None:
        """ Changes the fields position by calculating a new position by given movement

        :param movement: integer of pixel shift for x and y axis
        :return: None
        """
        pos_x = self.pos[0] + movement[0]
        pox_y = self.pos[1] + movement[1]
        self.pos = (pos_x, pox_y)

    def delete(self) -> None:
        """ Deletes the field

        :return: None
        """
        self.kill()
