""" This module provides an 'abstract' class for forms. Should not be used directly.

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.3'

import pygame


class Form(pygame.sprite.Sprite):
    def __init__(self, size: tuple[int, int]) -> None:
        """ Initializes basic class for form objects

        :param size: size of the form object
        """
        pygame.sprite.Sprite.__init__(self)

        self.LEFT = 0
        self.RIGHT = 1
        self.CENTER = 2
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.pos_x = 0
        self.pos_y = 0
        self.alignment = self.LEFT
        self.events = []
        self.sprite_sheet_handler = None

    def set_alpha(self, value):
        self.image.set_alpha(value)

    def set_colorkey(self, key: tuple[int, int, int]) -> None:
        """ Sets the colorkey of the image

        :param key: color to be set as the colorkey
        :return: None
        """
        self.image.set_colorkey(key)

    def get_events(self) -> list:
        """ Returns all raised form events without emptying the event queue

        :return: list of all raised form events
        """
        return self.events

    def clear_events(self) -> None:
        """ Empties the form event queue

        :return: None
        """
        self.events.clear()

    def handle_event(self, event) -> None:
        """ Handles given event

        :param event: pygame or resa event
        :return: None
        """
        pass

    def get_dimensions(self) -> tuple[int, int]:
        """ Returns form dimensions

        :return: size of the form image
        """
        return self.image.get_size()

    def width(self) -> int:
        """ Returns form width

        :return: width of the form image
        """
        return self.image.get_width()

    def height(self) -> int:
        """ Returns form height

        :return: height of the form image
        """
        return self.image.get_height()

    def align(self, alignment: int = None) -> None:
        """ Aligns the form horizontally in relation to its own position

        :param alignment: integer to set right, left or center
        :return: None
        """
        if alignment is None:
            alignment = self.alignment

        if alignment == self.RIGHT:
            self.rect.x = self.pos_x - self.rect.width
            self.rect.y = self.pos_y
        elif alignment == self.CENTER:
            self.rect.x = self.pos_x - self.rect.width / 2
            self.rect.y = self.pos_y
        elif alignment == self.LEFT:
            self.rect.x = self.pos_x
            self.rect.y = self.pos_y

        self.alignment = alignment
