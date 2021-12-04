""" This module provides classes to create worlds

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import random
import pygame

from data import settings
from data.world.field import Field
from data.world.nature import Tree
from data.handlers.spritesheet import SpriteSheetHandler, SpriteSheet


class Generator(object):
    def __init__(self, world_size: tuple[int, int], grid_size: tuple[int, int]) -> None:
        self.world_size = world_size
        self.grid_size = grid_size
        self.fields = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.rect = pygame.Rect(
            (0, 0),
            (self.world_size[0] * self.grid_size[0], self.world_size[1] * self.grid_size[1])
        )

        self.sprite_sheet_handler = SpriteSheetHandler()
        for key, value in settings.SPRITE_SHEETS_WORLD.items():
            sheet = SpriteSheet(key, value[0], value[1])
            sheet.colorkey = (0, 0, 0)
            self.sprite_sheet_handler.add(sheet)

    def get_world(self) -> tuple[pygame.sprite.Group, pygame.sprite.Group, pygame.Rect]:
        return self.fields, self.trees, self.rect

    def fill(self) -> None:
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

    def add_island(self, position: tuple[int, int]) -> None:
        island_data_set = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        sprite_sheet_solid = '0'
        sprite_sheet_transition = '3'

        # identify isometric x-shift and calculate top-left-position
        offset = divmod(len(island_data_set), 2)
        start_x = (position[0] + offset[0] + 1) * self.grid_size[0]
        start_y = position[1] * self.grid_size[1] - self.grid_size[1] / 2

        # run through island data set and add fields
        for row_nb, row in enumerate(island_data_set):
            for col_nb, tile in enumerate(row):
                solid = False
                if tile != 0:
                    # detecting fields around current field
                    neighbors = [
                        island_data_set[row_nb][col_nb - 1],  # left
                        island_data_set[row_nb][col_nb + 1],  # right
                        island_data_set[row_nb - 1][col_nb],  # top
                        island_data_set[row_nb + 1][col_nb],  # bottom
                        island_data_set[row_nb - 1][col_nb - 1],  # corner top left
                        island_data_set[row_nb - 1][col_nb + 1],  # corner top right
                        island_data_set[row_nb + 1][col_nb - 1],  # corner bottom left
                        island_data_set[row_nb + 1][col_nb + 1],  # corner bottom right
                    ]
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
                        sprite_index = 1
                        solid = True

                    # transform 2d position into isometric coordinates
                    # thanks to 'ThiPi' | https://python-forum.io/thread-14617.html
                    cart_x = row_nb * (self.grid_size[0] / 2)
                    cart_y = col_nb * self.grid_size[1]
                    pos_x = (cart_x - cart_y)
                    pos_y = (cart_x + cart_y) / 2

                    # delete possible duplicate
                    for field in self.fields:
                        if field.position() == (start_x + pos_x, start_y + pos_y):
                            field.delete()

                    # add field
                    if solid:
                        sprite_sheet = sprite_sheet_solid
                    else:
                        sprite_sheet = sprite_sheet_transition

                    image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
                    field = Field((int(start_x + pos_x), int(start_y + pos_y)), self.grid_size, image)
                    field.sprite_sheet_id = sprite_sheet
                    field.sprite_id = sprite_index
                    field.set_solid(solid)

                    self.fields.add(field)

        # add trees
        for field in self.fields:
            sprite_sheet = '14'

            if field.solid and random.randrange(0, 100, 1) >= 15:
                sprite_index = random.choice([0, 1, 2])
                image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
                pos = field.rect.bottomleft
                tree = Tree(pos, field.size, image)
                tree.sprite_sheet_id = sprite_sheet
                tree.sprite_id = sprite_index

                self.trees.add(tree)

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
