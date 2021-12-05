import random
import pygame.sprite
import data.world.islands.big_islands as big_islands
import data.world.islands.medium_islands as medium_islands
import data.world.islands.small_islands as small_islands


class Island(object):
    BIG = 0
    MEDIUM = 1
    SMALL = 2

    def __init__(self, position, size, temperature):
        self.position = position
        self.size = size
        self.temperature = temperature
        self.data_set = None
        self.data_fields = pygame.sprite.Group()

        self.__calc_data_set()

    def __calc_data_set(self):
        if self.size == 0:
            self.data_set = random.choice([
                big_islands.big_island_1,
                big_islands.big_island_2
            ])
        elif self.size == 1:
            self.data_set = random.choice([
                medium_islands.med_island_1,
                medium_islands.med_island_2,
                medium_islands.med_island_3
            ])
        elif self.size == 2:
            self.data_set = random.choice([
                small_islands.small_island_1,
                small_islands.small_island_2,
                small_islands.small_island_3,
                small_islands.small_island_4,
                small_islands.small_island_5
            ])
        else:
            self.data_set = [[1]]

