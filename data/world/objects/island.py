""" This module provides Island class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import random
import pygame.sprite
import data.world.islands.big_islands as big_islands
import data.world.islands.medium_islands as medium_islands
import data.world.islands.small_islands as small_islands
from data.settings import conf


class Island(object):
    BIG = 0
    MEDIUM = 1
    SMALL = 2

    def __init__(self, size, temperature):
        """ Creates an island.

        :param size: SMALL | MEDIUM | BIG
        :param temperature: temperature of the island
        """
        # basic settings
        self._size = size
        self._temperature = temperature
        self._data_set = None
        self._data_fields = pygame.sprite.Group()

        self.__calc_data_set()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if 0 >= value <= 2:
            self._size = value
        else:
            self._size = 0

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @property
    def data_set(self):
        return self._data_set

    @property
    def data_fields(self):
        return self._data_fields

    @data_fields.setter
    def data_fields(self, value):
        self._data_fields = value

    def calc_size(self) -> tuple[int, int]:
        """ Calculates width and height of the island in pixel.

        :return: width and height of the island
        """
        width_in_px = height_in_px = 0

        if self.data_set is not None:
            width_in_px = (len(self.data_set) + len(self.data_set[0])) * (conf.grid.width / 2)
            height_in_px = (len(self.data_set) + len(self.data_set[0])) * (conf.grid.height / 2)

        return width_in_px, height_in_px

    def __calc_data_set(self) -> None:
        """ Chooses randomly a data set for the island by its size.

        :return: None
        """
        if self.size == Island.BIG:
            self._data_set = random.choice([
                big_islands.big_island_1,
                big_islands.big_island_2
            ])
        elif self.size == Island.MEDIUM:
            self._data_set = random.choice([
                medium_islands.med_island_1,
                medium_islands.med_island_2,
                medium_islands.med_island_3
            ])
        else:
            self._data_set = random.choice([
                small_islands.small_island_1,
                small_islands.small_island_2,
                small_islands.small_island_3,
                small_islands.small_island_4,
                small_islands.small_island_5
            ])

    def __bool__(self):
        if len(self.data_fields) > 0:
            return True

        return False

    def __len__(self):
        return len(self.data_fields)

    def __str__(self):
        return f'Island - ' \
               f'Size px: {self.calc_size()} | ' \
               f'Size: {self.size} | ' \
               f'Temp: {self.temperature} | ' \
               f'Fields: {len(self.data_fields)}'

    def __repr__(self):
        return f'Island - ' \
               f'Size px: {self.calc_size()} | ' \
               f'Size: {self.size} | ' \
               f'Temp: {self.temperature} | ' \
               f'Fields: {len(self.data_fields)}'
