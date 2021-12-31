""" This module provides classes to create worlds

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""

from data.settings import conf
import random
import pygame
from data.interfaces.loadscreen import GameLoadScreen
from data.world.objects.field import Field
from data.world.entities.tree import Tree
from data.handlers.spritesheet import SpriteSheetHandler, SpriteSheet
from data.world.objects.island import Island
import data.world.grid

import data.world.islands.big_islands as big_islands


class Neighbors(object):
    def __init__(self):
        """ Dataclass for field data neighbors """
        self._left = False
        self._right = False
        self._top = False
        self._bottom = False
        self._topleft = False
        self._topright = False
        self._bottomleft = False
        self._bottomright = False

    @staticmethod
    def __value_check(value: int):
        if value == 1:
            return True

        return False

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value: int):
        self._left = self.__value_check(value)

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value: int):
        self._right = self.__value_check(value)

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value: int):
        self._top = self.__value_check(value)

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value: int):
        self._bottom = self.__value_check(value)

    @property
    def topleft(self):
        return self._topleft

    @topleft.setter
    def topleft(self, value: int):
        self._topleft = self.__value_check(value)

    @property
    def topright(self):
        return self._topright

    @topright.setter
    def topright(self, value: int):
        self._topright = self.__value_check(value)

    @property
    def bottomleft(self):
        return self._bottomleft

    @bottomleft.setter
    def bottomleft(self, value: int):
        self._bottomleft = self.__value_check(value)

    @property
    def bottomright(self):
        return self._bottomright

    @bottomright.setter
    def bottomright(self, value: int):
        self._bottomright = self.__value_check(value)


class Generator(object):
    def __init__(self) -> None:
        """ World generator """
        # world islands
        self.world_islands = {
            'North_West': Island(Island.MEDIUM, conf.temp_north),
            'North': Island(Island.SMALL, conf.temp_north),
            'North_East': Island(Island.MEDIUM, conf.temp_north),
            'Center_West': Island(Island.SMALL, conf.temp_center),
            'Center': Island(Island.BIG, conf.temp_center),
            'Center_East': Island(Island.SMALL, conf.temp_center),
            'South_West': Island(Island.MEDIUM, conf.temp_south),
            'South': Island(Island.SMALL, conf.temp_south),
            'South_East': Island(Island.MEDIUM, conf.temp_south),
        }

        # calculate world basic data by biggest island
        # todo: needs to be re-factored
        # fields_x, fields_y = self.world_islands['Center'].calc_size()
        fields_x, fields_y = (60, 40)

        # new grid
        conf.grid = data.world.grid.Grid(fields_x, fields_y, conf.grid_zoom)
        self.rect = pygame.Rect((0, 0), (conf.grid.grid_width, conf.grid.grid_height))

        # sprite groups
        self.water = pygame.sprite.Group()
        self.fields = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()

        # sprite sheets
        self.sprite_sheet_handler = SpriteSheetHandler()
        self.__load_sprite_sheets()

        # initialisize loading message
        self.load_msg = ""
        self.load_screen = GameLoadScreen(lambda: self.load_msg)

    def __load_sprite_sheets(self) -> None:
        """ Loads all sprite sheets by sprite sheet config list

        :return: None
        """
        for key, value in conf.sp_world.items():
            sheet = SpriteSheet(key, value[0], value[1])
            sheet.colorkey = None
            self.sprite_sheet_handler.add(sheet)

    def __update_load_screen(self) -> None:
        """ Updates the load screen. Calling it only after load message changed.

        :return: None
        """
        self.load_screen.run_logic()
        self.load_screen.render(pygame.display.get_surface())
        pygame.display.flip()

    def create(self) -> None:
        """ Create a world from scratch.

        :return: None
        """
        # fill world with water
        self.load_msg = 'Fill the world with water...'
        self.__update_load_screen()
        self.fill()
        # create islands
        self.load_msg = 'Creating islands...'
        self.__update_load_screen()
        self.__create_islands_new()
        # plant trees
        # self.load_msg = 'Planting trees...'
        # self.__update_load_screen()
        # self.__plant_trees()

    def get_world(self) -> tuple[pygame.sprite.Group, pygame.sprite.Group, pygame.sprite.Group, pygame.Rect]:
        """ Returns the world data. Sprite groups and rect.

        :return: worlds rect and all of its sprites
        """
        return self.water, self.fields, self.trees, self.rect

    def fill(self) -> None:
        # fresh start with solid water tiles
        self.water.empty()
        sprite_sheet = 'Tiles'
        sprite_index = 0

        for key, value in conf.grid.fields_iso.items():
            image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
            new_field = Field((value.rect.x, value.rect.y), image)
            new_field.sprite_sheet_id = sprite_sheet
            new_field.sprite_id = sprite_index
            new_field.solid = False
            # add to sprite group and go on
            self.water.add(new_field)

    def __create_islands_new(self):
        island = big_islands.big_island_1

        sprite_sheet = 'Tiles'
        temperature = conf.temp_north

        shift_left = 0
        shift_top = 3
        key = 1
        count = 0

        # shift left
        key += shift_left

        # shift top
        for i in range(shift_top):
            i -= 1
            if i % 2 == 0:
                key += (conf.grid.fields_x // 2)
            else:
                key += (conf.grid.fields_x // 2) - 1

        for row_nb, row in enumerate(island):
            for col_nb, tile in enumerate(row):
                if tile != 0:
                    pos_x = conf.grid.fields_iso[key].rect.x
                    pos_y = conf.grid.fields_iso[key].rect.y

                    # add field to island and global fields
                    image = self.sprite_sheet_handler.image_by_index(sprite_sheet, tile)
                    field = Field((int(pos_x), int(pos_y)), image)
                    field.sprite_sheet_id = sprite_sheet
                    field.sprite_id = tile
                    field.temperature = temperature
                    field.solid = True
                    self.fields.add(field)
                key += 1
                count += 1
            if row_nb % 2 == 0:
                key += (conf.grid.fields_x // 2) - count
            else:
                key += (conf.grid.fields_x // 2) - 1 - count
            count = 0

    # todo: needs to be re-factored
    def __create_islands(self) -> None:
        """ Uses world islands and calculate every field.

        :return: None
        """
        for key, island in self.world_islands.items():
            # identify isometric x-shift and calculate top-left-position
            start_x, start_y = self.calc_isometric_field_shift(island.data_set)

            # calculate island position
            pos_x, pos_y = self.__calc_island_position(island.calc_size(), key)
            start_x += pos_x
            start_y += pos_y

            # run through island data set and add fields
            for row_nb, row in enumerate(island.data_set):
                for col_nb, tile in enumerate(row):
                    # if tile is marked as 'water', ignore it
                    if tile == 0:
                        pass
                    else:
                        # detecting fields around current field to get sprite index
                        neighbors = Neighbors()
                        neighbors.left = island.data_set[row_nb][col_nb - 1]
                        neighbors.right = island.data_set[row_nb][col_nb + 1]
                        neighbors.top = island.data_set[row_nb - 1][col_nb]
                        neighbors.bottom = island.data_set[row_nb + 1][col_nb]
                        neighbors.topleft = island.data_set[row_nb - 1][col_nb - 1]
                        neighbors.topright = island.data_set[row_nb - 1][col_nb + 1]
                        neighbors.bottomleft = island.data_set[row_nb + 1][col_nb - 1]
                        neighbors.bottomright = island.data_set[row_nb + 1][col_nb + 1]
                        sprite_index, rotate = self.calc_field_transition_sprite_index(neighbors)

                        # calc sprite sheets and solid attribute
                        if sprite_index is None:
                            # solid tiles
                            if island.temperature == conf.temp_north:
                                sprite_index = 1
                            elif island.temperature == conf.temp_south:
                                sprite_index = 2
                            else:
                                sprite_index = 1
                            sprite_sheet = 'Tiles'
                            solid = True
                        else:
                            # water transition tiles
                            if island.temperature == conf.temp_north:
                                sprite_sheet = 'Tiles'
                            elif island.temperature == conf.temp_south:
                                sprite_sheet = 'Tiles'
                            else:
                                sprite_sheet = 'Tiles'
                            solid = False

                        # transform 2d position into isometric coordinates
                        pos_x, pos_y = self.isometric_transform((row_nb, col_nb))

                        # add field to island and global fields
                        image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
                        if rotate:
                            image = pygame.transform.rotate(image, 180)
                        field = Field((int(start_x + pos_x), int(start_y + pos_y)), image)
                        field.sprite_sheet_id = sprite_sheet
                        field.sprite_id = sprite_index
                        field.temperature = island.temperature
                        field.solid = solid
                        self.world_islands[key].data_fields.add(field)
                        self.fields.add(field)

    def __plant_trees(self) -> None:
        """ Goes through every field and plants a tree under some conditions.

        :return: None
        """
        for field in self.fields:
            sprite_sheet = None
            sprite_index = 0
            # only plant trees on solid fields
            if field.solid:
                # central islands get broadleafs by chance
                if field.temperature == conf.temp_center and random.randrange(0, 100, 1) <= conf.tree_spawn_bl:
                    sprite_sheet = 'Trees'
                    sprite_index = random.choice([0, 6, 12])
                    plant = True
                # north islands get evergreens by chance
                elif field.temperature == conf.temp_north and random.randrange(0, 100, 1) <= conf.tree_spawn_eg:
                    sprite_sheet = 'Trees'
                    sprite_index = random.choice([0, 6, 12])
                    plant = True
                # south islands get palms by chance
                elif field.temperature == conf.temp_south and random.randrange(0, 100, 1) <= conf.tree_spawn_p:
                    sprite_sheet = 'Trees'
                    sprite_index = random.choice([0, 6, 12])
                    plant = True
                else:
                    plant = False

                if plant:
                    image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
                    pos = field.rect.bottomleft
                    tree = Tree(pos, image)
                    tree.sprite_sheet_id = sprite_sheet
                    tree.sprite_id = sprite_index
                    self.trees.add(tree)

    # todo: needs to be re-factored
    def __calc_island_position(self, island_size: tuple[int, int], key: str) -> tuple[int, int]:
        """ Calculates islands sector position and center it in its sector.

        :param island_size: width and height of the island
        :param key: island sector key
        :return: None
        """
        pos_x = pos_y = 0
        island_width, island_height = island_size
        sector_width = self.world_size[0] / 3
        sector_height = self.world_size[1] / 3

        # calculate central position in sector
        diff_x = int(((sector_width - island_width) / conf.grid.width) / 2) * conf.grid.width
        diff_y = int(((sector_height - island_height) / conf.grid.height) / 2)
        if diff_y % 2 == 0:
            diff_y = diff_y * conf.grid.height / 2
        else:
            diff_y = (diff_y + 1) * conf.grid.height / 2
        pos_x += diff_x
        # isometric double row
        pos_y += diff_y * 2

        # calculate sector shift by its sector key
        if key == 'North':
            pos_x += sector_width
        elif key == 'North_East':
            pos_x += sector_width * 2
        elif key == 'Center_West':
            pos_y += sector_height
        elif key == 'Center':
            pos_y += sector_height
            pos_x += sector_width
        elif key == 'Center_East':
            pos_y += sector_height
            pos_x += sector_width * 2
        elif key == 'South_West':
            pos_y += sector_height * 2
        elif key == 'South':
            pos_y += sector_height * 2
            pos_x += sector_width
        elif key == 'South_East':
            pos_y += sector_height * 2
            pos_x += sector_width * 2
        else:
            pass

        return pos_x, pos_y

    # todo: needs to be re-factored
    @staticmethod
    def calc_field_transition_sprite_index(neighbors: Neighbors) -> tuple[int, bool]:
        """ Calculates sprite index by the neighbor fields of a field.

        :param neighbors: list of neighbor fields from island data
        :return: sprite index
        """
        rotate = False
        # sides
        if neighbors.left and neighbors.right and not neighbors.top and neighbors.bottom:
            sprite_index = 9
            rotate = True
        elif not neighbors.left and neighbors.right and neighbors.top and neighbors.bottom:
            sprite_index = 8
        elif neighbors.left and not neighbors.right and neighbors.top and neighbors.bottom:
            sprite_index = 8
            rotate = True
        elif neighbors.left and neighbors.right and neighbors.top and not neighbors.bottom:
            sprite_index = 9
        # inner corner
        elif neighbors.left and not neighbors.right and neighbors.top and not neighbors.bottom:
            sprite_index = 13
            rotate = True
        elif not neighbors.left and neighbors.right and not neighbors.top and neighbors.bottom:
            sprite_index = 13
        elif neighbors.left and not neighbors.right and not neighbors.top and neighbors.bottom:
            sprite_index = 12
            rotate = True
        elif not neighbors.left and neighbors.right and neighbors.top and not neighbors.bottom:
            sprite_index = 12
        # inner corner side
        elif not neighbors.bottomright and neighbors.left and neighbors.top:
            sprite_index = 11
            rotate = True
        elif not neighbors.topleft and neighbors.left and neighbors.top:
            sprite_index = 11
        elif not neighbors.bottomleft and neighbors.left and neighbors.top:
            sprite_index = 10
        elif not neighbors.topright and neighbors.left and neighbors.top:
            sprite_index = 10
            rotate = True
        else:
            sprite_index = None

        return sprite_index, rotate

    # todo: needs to be re-factored
    @staticmethod
    def calc_isometric_field_shift(data_set: list) -> tuple[int, int]:
        """ Calculates the isometric field shift (left shift)

        :param data_set: islands data set
        :return: topleft position to start with
        """
        if len(data_set) % 2 == 0:
            start_x = (len(data_set) - 1) * conf.grid.width / 2
        else:
            start_x = (len(data_set)) * conf.grid.width / 2
        start_y = 0

        return start_x, start_y

    # todo: needs to be re-factored
    @staticmethod
    def isometric_transform(row_col: tuple[int, int]) -> tuple[int, int]:
        """ Transforms 2d position into isometric coordinates.

        :param row_col: row and col pair of the field
        :return: position of the field
        :credit: 'ThiPi' | https://python-forum.io/thread-14617.html
        """
        row_nb, col_nb = row_col
        cart_x = col_nb * (conf.grid.width / 2)
        cart_y = row_nb * conf.grid.height
        pos_x = (cart_x - cart_y)
        pos_y = (cart_x + cart_y) / 2

        return pos_x, pos_y

    def load_fields_by_dict(self, fields_data: dict) -> None:
        """ Loads fields as sprites into sprite group by their raw data set.

        :param fields_data: fields with raw data set
        :return: None
        """
        self.fields.empty()
        for field_data in fields_data:
            image = self.sprite_sheet_handler.image_by_index(field_data.sprite_sheet, field_data.sprite_index)
            field = Field(field_data.pos, image)
            field.sprite_sheet_id = field_data.sprite_sheet
            field.sprite_id = field_data.sprite_index
            field.solid = field_data.solid

            self.fields.add(field)

    def load_trees_by_dict(self, trees_data: dict) -> None:
        """ Loads trees as sprites into sprite group by their raw data set.

        :param trees_data: trees with raw data set
        :return: None
        """
        self.trees.empty()
        for tree_data in trees_data:
            image = self.sprite_sheet_handler.image_by_index(tree_data.sprite_sheet, tree_data.sprite_index)
            tree = Tree(tree_data.pos, image)
            tree.sprite_sheet_id = tree_data.sprite_sheet
            tree.sprite_id = tree_data.sprite_index

            self.trees.add(tree)
