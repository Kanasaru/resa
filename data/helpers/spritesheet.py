""" This module provides sprite sheet handling by class SpriteSheet

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
:contribution: code is taken and slightly edited from https://www.pygame.org/wiki/Spritesheet
"""

__version__ = '1.0'

import logging
import pygame


class SpriteSheet(object):
    def __init__(self, filename: str) -> None:
        """ Initializes a sprite sheet

        :param filename: pathname to sprite sheet
        """
        try:
            self.sheet = pygame.image.load(filename).convert()
            self.sheet_size = self.sheet.get_size()
        except FileNotFoundError as e:
            logging.error(e)
            self.sheet = pygame.Surface((0, 0))

    def image_at(self, rectangle: tuple[int, int, int, int], colorkey: tuple[int, int, int] = None) -> pygame.Surface:
        """ Returns an image from the sprite sheet by given rectangle and colorkey

        :param rectangle: position and size of the image on the sprite sheet
        :param colorkey: colorkey that is used to create the images
        :return: selected image
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    def image_rotate(self, image: pygame.Surface, angle: int) -> pygame.Surface:
        """ Rotates given image by given angle and returns the new image

        :param image: image that should be transformed
        :param angle: angle used to transform the image
        :return: created image
        """
        image_new = pygame.transform.rotate(image, angle)
        return image_new

    def images_at(self, rects: list, colorkey: tuple[int, int, int] = None) -> list[pygame.Surface]:
        """ Returns a list of images located at given rectangles

        :param rects: list of rectangles
        :param colorkey: colorkey that is used to create the images
        :return: list of images
        """
        return [self.image_at(rect, colorkey) for rect in rects]
