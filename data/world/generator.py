""" This module provides classes to create worlds

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import random
import pygame

from data import settings
from data.world.objects.field import Field
from data.world.entities.tree import Tree
from data.handlers.spritesheet import SpriteSheetHandler, SpriteSheet
from data.world.objects.island import Island


class Generator(object):
    def __init__(self, grid_size: tuple[int, int]) -> None:
        self.world_size = (70, 60)
        self.grid_size = grid_size
        self.fields = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.rect = pygame.Rect(
            (0, 0),
            (self.world_size[0] * self.grid_size[0], self.world_size[1] * self.grid_size[1])
        )
        self.sprite_sheet_handler = None

        self.__load_sprite_sheets()

    def __load_sprite_sheets(self):
        self.sprite_sheet_handler = SpriteSheetHandler()
        for key, value in settings.SPRITE_SHEETS_WORLD.items():
            sheet = SpriteSheet(key, value[0], value[1])
            sheet.colorkey = (0, 0, 0)
            self.sprite_sheet_handler.add(sheet)

    def create(self):
        # fill world with water
        print('Fill world with water...')
        self.__fill()
        # create islands
        print('Create islands...')
        self.__create_islands()
        # raise mountains
        print('Raise mountains...')
        # plant trees
        print('Plant trees...')
        self.__plant_trees()

    def get_world(self) -> tuple[pygame.sprite.Group, pygame.sprite.Group, pygame.Rect]:
        return self.fields, self.trees, self.rect

    def __fill(self) -> None:
        self.fields.empty()
        sprite_sheet = '0'
        sprite_index = 5

        pos_x = self.grid_size[0] / 2
        pos_y = 0
        for row in range(self.world_size[1] * 2 - 1):
            for col in range(self.world_size[0]):
                image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
                new_field = Field((pos_x, pos_y), self.grid_size, image)
                new_field.sprite_sheet_id = sprite_sheet
                new_field.sprite_id = sprite_index
                self.fields.add(new_field)
                pos_x += self.grid_size[0]
            pos_y += self.grid_size[1] / 2
            if (row % 2) == 0:
                pos_x = 0
            else:
                pos_x = self.grid_size[0] / 2

    def __create_islands(self):
        # islands in world
        world_islands = {
            'North_West': Island((0, 0), Island.MEDIUM, -20),
            'North': Island((20, 0), Island.SMALL, -20),
            'North_East': Island((40, 0), Island.MEDIUM, -20),
            'Center_West': Island((0, 20), Island.SMALL, 20),
            'Center': Island((20, 20), Island.BIG, 20),
            'Center_East': Island((40, 20), Island.SMALL, 20),
            'South_West': Island((0, 40), Island.MEDIUM, 40),
            'South': Island((20, 40), Island.SMALL, 40),
            'South_East': Island((40, 40), Island.MEDIUM, 40),
        }

        # create data fields
        for key, island in world_islands.items():
            # identify isometric x-shift and calculate top-left-position
            start_x, start_y = self.calc_isometric_field_shift(island.data_set, island.position, self.grid_size)

            # run through island data set and add fields
            for row_nb, row in enumerate(island.data_set):
                for col_nb, tile in enumerate(row):
                    if tile != 0:
                        # detecting fields around current field
                        neighbors = [
                            island.data_set[row_nb][col_nb - 1],  # left
                            island.data_set[row_nb][col_nb + 1],  # right
                            island.data_set[row_nb - 1][col_nb],  # top
                            island.data_set[row_nb + 1][col_nb],  # bottom
                            island.data_set[row_nb - 1][col_nb - 1],  # corner top left
                            island.data_set[row_nb - 1][col_nb + 1],  # corner top right
                            island.data_set[row_nb + 1][col_nb - 1],  # corner bottom left
                            island.data_set[row_nb + 1][col_nb + 1],  # corner bottom right
                        ]
                        sprite_index = self.calc_field_transition_sprite_index(neighbors)

                        # calc sprite sheets and solid attribute
                        if sprite_index is None:
                            # solid tiles
                            if island.temperature == -20:
                                sprite_index = 0
                            elif island.temperature == 40:
                                sprite_index = 4
                            else:
                                sprite_index = 1
                            sprite_sheet = '0'
                            solid = True
                        else:
                            # water transition tiles
                            if island.temperature == -20:
                                sprite_sheet = '2'
                            elif island.temperature == 40:
                                sprite_sheet = '5'
                            else:
                                sprite_sheet = '1'
                            solid = False

                        # transform 2d position into isometric coordinates
                        pos_x, pos_y = self.isometric_transform((row_nb, col_nb), self.grid_size)

                        # add field to island
                        image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
                        field = Field((int(start_x + pos_x), int(start_y + pos_y)), self.grid_size, image)
                        field.sprite_sheet_id = sprite_sheet
                        field.sprite_id = sprite_index
                        field.temperature = island.temperature
                        field.set_solid(solid)
                        world_islands[key].data_fields.add(field)

                        # delete possible duplicate and replace it
                        for island_field in island.data_fields:
                            for field in self.fields:
                                if field.position() == island_field.position():
                                    field.delete()
                                    self.fields.add(island_field)

    def __plant_trees(self):
        for field in self.fields:
            if field.solid:
                plant = True
                if field.temperature == 20 and random.randrange(0, 100, 1) >= 30:
                    sprite_sheet = '14'
                    sprite_index = random.choice([0, 1, 2])
                elif field.temperature == -20 and random.randrange(0, 100, 1) >= 15:
                    sprite_sheet = '15'
                    sprite_index = random.choice([0, 1, 2, 3, 4, 5])
                elif field.temperature == 40 and random.randrange(0, 100, 1) >= 30:
                    sprite_sheet = '16'
                    sprite_index = random.choice([0, 1, 2])
                else:
                    plant = False

                if plant:
                    image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
                    pos = field.rect.bottomleft
                    tree = Tree(pos, field.size, image)
                    tree.sprite_sheet_id = sprite_sheet
                    tree.sprite_id = sprite_index
                    self.trees.add(tree)

    @staticmethod
    def calc_field_transition_sprite_index(neighbors):
        # sides
        if neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1:
            sprite_index = random.choice([24, 28, 32, 36, 40])
        elif neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 1:
            sprite_index = random.choice([25, 29, 33, 37, 41])
        elif neighbors[0] == 1 and neighbors[1] == 0 and neighbors[2] == 1 and neighbors[3] == 1:
            sprite_index = random.choice([26, 30, 34, 38, 42])
        elif neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 0:
            sprite_index = random.choice([27, 31, 35, 39, 43])
        # inner corner
        elif neighbors[0] == 1 and neighbors[1] == 0 and neighbors[2] == 1 and neighbors[3] == 0:
            sprite_index = random.choice([0, 4, 8])
        elif neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1:
            sprite_index = random.choice([1, 5, 9])
        elif neighbors[0] == 1 and neighbors[1] == 0 and neighbors[2] == 0 and neighbors[3] == 1:
            sprite_index = random.choice([2, 6, 10])
        elif neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 0:
            sprite_index = random.choice([3, 7, 11])
        # inner corner side
        elif neighbors[7] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
            sprite_index = random.choice([12, 16])
        elif neighbors[4] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
            sprite_index = random.choice([13, 17])
        elif neighbors[6] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
            sprite_index = random.choice([14, 18])
        elif neighbors[5] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
            sprite_index = random.choice([15, 19])
        else:
            sprite_index = None

        return sprite_index

    @staticmethod
    def calc_isometric_field_shift(data_set, position, grid_size):
        offset = divmod(len(data_set), 2)
        start_x = (position[0] + offset[0] + 1) * grid_size[0]
        start_y = position[1] * grid_size[1] - grid_size[1] / 2

        return start_x, start_y

    @staticmethod
    def isometric_transform(row_col, grid_size):
        # transform 2d position into isometric coordinates
        # thanks to 'ThiPi' | https://python-forum.io/thread-14617.html
        row_nb, col_nb = row_col
        cart_x = row_nb * (grid_size[0] / 2)
        cart_y = col_nb * grid_size[1]
        pos_x = (cart_x - cart_y)
        pos_y = (cart_x + cart_y) / 2

        return pos_x, pos_y

    def load_fields_by_dict(self, fields_data: dict) -> None:
        self.fields.empty()
        for field_data in fields_data:
            pos = field_data[0]
            sprite_sheet = field_data[1][0]
            sprite_index = field_data[1][1]
            solid = field_data[2]
            image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
            field = Field(pos, self.grid_size, image)
            field.sprite_sheet_id = sprite_sheet
            field.sprite_id = sprite_index
            field.set_solid(solid)

            self.fields.add(field)

    def load_trees_by_dict(self, trees_data: dict) -> None:
        self.trees.empty()
        for tree_data in trees_data:
            pos = tree_data[0]
            sprite_sheet = tree_data[1][0]
            sprite_index = tree_data[1][1]
            image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
            tree = Tree(pos, self.grid_size, image)
            tree.sprite_sheet_id = sprite_sheet
            tree.sprite_id = sprite_index

            self.trees.add(tree)
