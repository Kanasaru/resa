import random
import pygame.sprite
import data.world.islands.big_islands as big_islands
import data.world.islands.medium_islands as medium_islands
import data.world.islands.small_islands as small_islands


class Island(object):
    BIG = 0
    MEDIUM = 1
    SMALL = 2

    def __init__(self, size, temperature):
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

    def calc_size(self):
        grid_size = (40, 20)
        width_in_px = height_in_px = 0
        if self.data_set is not None:
            # only works with even len result...need to re-think
            width_in_px = (len(self.data_set) + len(self.data_set[0])) * (grid_size[0] / 2)
            height_in_px = (len(self.data_set) + len(self.data_set[0])) * (grid_size[1] / 2)
        return width_in_px, height_in_px

    def __calc_data_set(self):
        if self.size == 0:
            self._data_set = random.choice([
                big_islands.big_island_1,
                big_islands.big_island_2
            ])
        elif self.size == 1:
            self._data_set = random.choice([
                medium_islands.med_island_1,
                medium_islands.med_island_2,
                medium_islands.med_island_3
            ])
        elif self.size == 2:
            self._data_set = random.choice([
                small_islands.small_island_1,
                small_islands.small_island_2,
                small_islands.small_island_3,
                small_islands.small_island_4,
                small_islands.small_island_5
            ])
        else:
            self._data_set = [[1]]

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
