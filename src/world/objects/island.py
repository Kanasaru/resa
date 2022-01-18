""" This module provides Island class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pickle
import random

BIG = 0
MEDIUM = 1
SMALL = 2


class Island(object):
    def __init__(self, size, temperature):
        """ Creates an island.

        :param size: SMALL | MEDIUM | BIG
        :param temperature: temperature of the island
        """
        # basic settings
        self._size = size
        self._temperature = temperature
        self._data_set = None
        self.data_fields = []
        self.mountains = []

        self.load_island_from_file()

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

    def load_island_from_file(self) -> None:
        number = random.choice([1])
        size = ''
        if self.size == BIG:
            size = 'b'
        elif self.size == MEDIUM:
            size = 'm'
        else:
            size = 's'
        self.data_fields = pickle.load(open(f'data/islands/{size}_{number}.island', 'rb'))

    def __bool__(self):
        if len(self.data_fields) > 0:
            return True

        return False

    def __len__(self):
        return len(self.data_fields)

    def __str__(self):
        return f'Island - ' \
               f'Size: {self.size} | ' \
               f'Temp: {self.temperature} | ' \
               f'Fields: {len(self.data_fields)}'

    def __repr__(self):
        return f'Island - ' \
               f'Size: {self.size} | ' \
               f'Temp: {self.temperature} | ' \
               f'Fields: {len(self.data_fields)}'
