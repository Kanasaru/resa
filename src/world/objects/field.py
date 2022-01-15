""" This module provides Field class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
from src.handler import RESA_CH, RESA_EH


class RawField(object):
    def __init__(self):
        """ Dataclass for raw fields """
        self.pos = None
        self.sprite_index = None
        self.sprite_sheet = None
        self.solid = None
        self.iso_key = None
        self.rect = None
        self.temperature = None

        self.sprite = None
        self.buildable = False
        self.building = False


class Field(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], image: pygame.image) -> None:
        """ Initializes a field

        :param position: position on world surface
        :param image: field image
        """
        pygame.sprite.Sprite.__init__(self)

        # basic settings
        self.size = (RESA_CH.grid_zoom * 2, RESA_CH.grid_zoom)
        self.visible = True
        self.temperature = RESA_CH.temp_center
        self.solid = False

        # image and sprite settings
        self.image = pygame.transform.scale(image, self.size).convert_alpha()
        self.sprite_sheet_id = None
        self.sprite_id = None

        self.iso_key = -1

        # positions
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def update(self, event: pygame.event.Event = None) -> None:
        """ Updates field by its position

        :param event: optional event
        :return: None
        """
        if event is not None:
            if event.type == RESA_EH.RESA_GAME_EVENT:
                if event.code == RESA_EH.RESA_CTRL_MAP_MOVE:
                    self.position = (self.position[0] + event.move[0], self.position[1] + event.move[1])
        self.rect.topleft = self.position

    def delete(self) -> None:
        """ Deletes the field

        :return: None
        """
        self.kill()

    def __str__(self):
        return f'Field - ' \
               f'Pos: {self.position} | ' \
               f'Solid: {self.solid} | ' \
               f'Temp: {self.temperature} | ' \
               f'Visible: {self.visible}'

    def __repr__(self):
        return f'Field - ' \
               f'Pos: {self.position} | ' \
               f'Solid: {self.solid} | ' \
               f'Temp: {self.temperature} | ' \
               f'Visible: {self.visible}'
