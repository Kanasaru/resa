""" This module provides classes to create worlds

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '0.1'

import random
import pygame
from data.world.field import Field
from data.helpers.spritesheet import SpriteSheet


class Generator(object):
    def __init__(self, world_size: tuple[int, int], grid_size: tuple[int, int]) -> None:
        """ Creates basic world and its parameters

        :param world_size: width and height as number of fields of the world
        :param grid_size: width and height in px as size of used tile-grid
        """
        self.world_size = world_size
        self.grid_size = grid_size
        self.fields = pygame.sprite.Group()
        self.rect = pygame.Rect(
            (0, 0),
            (self.world_size[0] * self.grid_size[0], self.world_size[1] * self.grid_size[1])
        )
        self.sprite_sheets = []
        self.field_dict = {}
        self.field_dict_id = 0

    def get_world(self) -> tuple[pygame.sprite.Group, pygame.Rect]:
        """ Returns the generated world values

        :return: sprites and rectangle of the created world
        """
        return self.fields, self.rect

    def add_sprite_sheet(self, sprite_sheet: str) -> None:
        """ Adds a sprite sheet that can be used for world generation

        :param sprite_sheet: path to a sprite map/sheet
        :return: None
        """
        self.sprite_sheets.append(SpriteSheet(sprite_sheet))

    def set_field_dict(self, field_dict: dict) -> None:
        """ Sets the field dict as reference dictionary for added sprite sheets

        :param field_dict:
        :return: None
        """
        self.field_dict = field_dict

    def fill(self, field_dict_id: int) -> None:
        """ Uses given id to create all fields of the world

        :param field_dict_id: id of a field in field dictionary, set by set_field_dict
        :return: None
        """
        self.fields.empty()
        self.field_dict_id = field_dict_id

        pos_x = self.grid_size[0] / 2
        pos_y = 0
        for row in range(self.world_size[1] * 2 - 1):
            for col in range(self.world_size[0]):
                image = self.sprite_sheets[self.get_sprite_sheet_id("Water", self.field_dict_id)].image_at(
                    self.field_dict[self.field_dict_id]["sprite_rect"],
                    self.field_dict[self.field_dict_id]["colorkey"]
                )
                self.fields.add(Field((pos_x, pos_y), self.grid_size, image))
                pos_x += self.grid_size[0]
            pos_y += self.grid_size[1] / 2
            if (row % 2) == 0:
                pos_x = 0
            else:
                pos_x = self.grid_size[0] / 2

    def get_sprite_sheet_id(self, name: str, field_dict_id: int) -> int:
        """ Returns an id of a sprite sheet by comparing wished sheet with fields dictionary sheets

        :param name: name that will be compared with names dictionary
        :param field_dict_id: id from fields dictionary
        :return: sprite sheet id that was identified by name
        :todo: needs a lot improvement (o.O)
        """
        sheet_names = {"Dirt A": 1, "Dirt B": 2, "Grass A": 3, "Grass B": 4, "Sand": 5, }
        sprite_sheet_id = self.field_dict[field_dict_id]["sprite_sheet"]
        if isinstance(sprite_sheet_id, tuple):
            for sheet_id in sprite_sheet_id:
                try:
                    if sheet_names[name] == sheet_id:
                        return sheet_id
                finally:
                    pass
            print("ERROR: Given name not allowed with field identifier")
            return 0
        else:
            return sprite_sheet_id

    def add_island(self, position: tuple[int, int], island_data_set: dict) -> None:
        """ Adds an island to the world

        :param position: top and left position the island should be placed
        :param island_data_set: data set of the island
        :return: None
        """
        solid_tile = "Grass A"
        water_to_solid = "Dirt B"

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
                        field_dict_id = random.choice([30, 34, 38, 42, 46])
                    elif neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 1:
                        field_dict_id = random.choice([31, 35, 39, 43, 47])
                    elif neighbors[0] == 1 and neighbors[1] == 0 and neighbors[2] == 1 and neighbors[3] == 1:
                        field_dict_id = random.choice([32, 36, 40, 44, 48])
                    elif neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 0:
                        field_dict_id = random.choice([33, 37, 41, 45, 49])
                    # inner corner
                    elif neighbors[0] == 1 and neighbors[1] == 0 and neighbors[2] == 1 and neighbors[3] == 0:
                        field_dict_id = random.choice([6, 10, 14])
                    elif neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1:
                        field_dict_id = random.choice([7, 11, 15])
                    elif neighbors[0] == 1 and neighbors[1] == 0 and neighbors[2] == 0 and neighbors[3] == 1:
                        field_dict_id = random.choice([8, 12, 16])
                    elif neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 0:
                        field_dict_id = random.choice([9, 13, 17])
                    # inner corner side
                    elif neighbors[7] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
                        field_dict_id = random.choice([18, 22])
                    elif neighbors[4] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
                        field_dict_id = random.choice([19, 23])
                    elif neighbors[6] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
                        field_dict_id = random.choice([20, 24])
                    elif neighbors[5] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
                        field_dict_id = random.choice([21, 25])
                    else:
                        field_dict_id = 1
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
                    image = self.sprite_sheets[self.get_sprite_sheet_id(water_to_solid, field_dict_id)].image_at(
                        self.field_dict[field_dict_id]["sprite_rect"],
                        self.field_dict[field_dict_id]["colorkey"]
                    )
                    field = Field((int(start_x + pos_x), int(start_y + pos_y)), self.grid_size, image)
                    field.set_solid(solid)

                    self.fields.add(field)
