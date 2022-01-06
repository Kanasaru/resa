""" This module provides classes to create worlds

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pickle

from data.handlers.locals import LocalsHandler
from data.settings import conf
import random
import pygame
from data.interfaces.loadscreen import GameLoadScreen
from data.world.objects.field import RawField, Field
from data.world.entities.tree import Tree
from data.handlers.spritesheet import SpriteSheetHandler, SpriteSheet
import data.world.objects.island as islands
import data.world.grid


class World(object):
    def __init__(self, grid_x, grid_y):
        self.grid = conf.grid = data.world.grid.Grid(grid_x, grid_y, conf.grid_zoom)
        self.rect = pygame.Rect((0, 0), (self.grid.grid_width, self.grid.grid_height))
        self.image = pygame.Surface(self.rect.size)
        self.grid_image = pygame.Surface(self.rect.size)
        self.grid_fields = {}
        self.entities = pygame.sprite.Group()
        self.islands = None


class Generator(object):
    def __init__(self) -> None:
        """ World generator """
        self.world = World(132, 132)

        # world islands
        self.world.islands = {
            'North_West': islands.Island(islands.MEDIUM, conf.temp_north),
            'North': islands.Island(islands.SMALL, conf.temp_north),
            'North_East': islands.Island(islands.MEDIUM, conf.temp_north),
            'Center_West': islands.Island(islands.SMALL, conf.temp_center),
            'Center': islands.Island(islands.BIG, conf.temp_center),
            'Center_East': islands.Island(islands.SMALL, conf.temp_center),
            'South_West': islands.Island(islands.MEDIUM, conf.temp_south),
            'South': islands.Island(islands.SMALL, conf.temp_south),
            'South_East': islands.Island(islands.MEDIUM, conf.temp_south),
        }

        self.fields = pygame.sprite.Group()

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
        self.load_msg = f"{LocalsHandler.lang('load_world_water')}"
        self.__update_load_screen()
        self.fill()
        # create islands
        self.load_msg = f"{LocalsHandler.lang('load_world_islands')}"
        self.__update_load_screen()
        self.__create_islands()
        # background
        self.__world_image()
        # plant trees
        self.load_msg = f"{LocalsHandler.lang('load_world_trees')}"
        self.__update_load_screen()
        self.__plant_trees()

    def __world_image(self):
        self.fields.draw(self.world.image)
        self.fields.draw(self.world.grid_image)
        self.world.grid.draw_iso_grid(self.world.grid_image, (0, 0))

    def get_world(self) -> World:
        """ Returns the world data.

        :return: a world
        """
        return self.world

    def fill(self) -> None:
        # fresh start with solid water tiles
        self.fields.empty()
        sprite_sheet = 'Tiles'
        sprite_index = 2

        for key, value in conf.grid.fields_iso.items():
            image = self.sprite_sheet_handler.image_by_index(sprite_sheet, sprite_index)
            new_field = Field((value.rect.x, value.rect.y), image)
            new_field.sprite_sheet_id = sprite_sheet
            new_field.sprite_id = sprite_index
            new_field.solid = False

            raw_field = RawField()
            raw_field.rect = value.rect
            raw_field.iso_key = value.key
            raw_field.sprite_sheet = sprite_sheet
            raw_field.sprite_index = sprite_index
            raw_field.solid = False
            self.world.grid_fields[key] = raw_field

            # add to sprite group and go on
            self.fields.add(new_field)

    def __create_islands(self):
        field_shift = 44

        for key, value in self.world.islands.items():
            if key == 'North_West':
                nc_key = 1
                temperature = conf.temp_north
            elif key == 'North':
                nc_key = 23
                temperature = conf.temp_north
            elif key == 'North_East':
                nc_key = 45
                temperature = conf.temp_north
            elif key == 'Center_West':
                nc_key = 5765
                temperature = conf.temp_center
            elif key == 'Center':
                nc_key = 5787
                temperature = conf.temp_center
            elif key == 'Center_East':
                nc_key = 5809
                temperature = conf.temp_center
            elif key == 'South_West':
                nc_key = 11529
                temperature = conf.temp_south
            elif key == 'South':
                nc_key = 11551
                temperature = conf.temp_south
            elif key == 'South_East':
                nc_key = 11573
                temperature = conf.temp_south
            else:
                raise KeyError(f'Which island should that be, called {key}?')

            row_even = True
            col_count = 1

            for field_data in value.data_fields:
                if row_even:
                    if col_count <= conf.grid.fields_x // 6:
                        if field_data.sprite_index != 2:
                            image = self.sprite_sheet_handler.image_by_index(field_data.sprite_sheet, field_data.sprite_index)
                            field = Field(self.world.grid.fields_iso[nc_key].rect.topleft, image)
                            field.sprite_sheet_id = field_data.sprite_sheet
                            field.sprite_id = field_data.sprite_index
                            field.solid = field_data.solid
                            field.iso_key = nc_key
                            field.temperature = temperature

                            raw_field = RawField()
                            raw_field.rect = self.world.grid.fields_iso[nc_key].rect
                            raw_field.iso_key = field.iso_key
                            raw_field.sprite_sheet = field_data.sprite_sheet
                            raw_field.sprite_index = field_data.sprite_index
                            raw_field.temperature = temperature
                            if 2 < field_data.sprite_index < 5:
                                raw_field.solid = True
                                field.solid = True
                            else:
                                raw_field.solid = False
                                field.solid = False

                            self.fields.add(field)
                            self.world.grid_fields[key] = raw_field

                        col_count += 1
                    else:
                        nc_key += field_shift
                        col_count = 1
                        row_even = False

                        if nc_key in conf.grid.fields_iso:
                            pass
                        else:
                            break

                if not row_even:
                    if col_count <= conf.grid.fields_x // 6 - 1:
                        if field_data.sprite_index != 2:
                            image = self.sprite_sheet_handler.image_by_index(field_data.sprite_sheet, field_data.sprite_index)
                            field = Field(self.world.grid.fields_iso[nc_key].rect.topleft, image)
                            field.sprite_sheet_id = field_data.sprite_sheet
                            field.sprite_id = field_data.sprite_index
                            field.solid = field_data.solid
                            field.iso_key = nc_key
                            field.temperature = temperature

                            raw_field = RawField()
                            raw_field.rect = self.world.grid.fields_iso[nc_key].rect
                            raw_field.iso_key = field.iso_key
                            raw_field.sprite_sheet = field_data.sprite_sheet
                            raw_field.sprite_index = field_data.sprite_index
                            raw_field.temperature = temperature
                            if 2 < field_data.sprite_index < 5:
                                raw_field.solid = True
                                field.solid = True
                            else:
                                raw_field.solid = False
                                field.solid = False

                            self.fields.add(field)
                            self.world.grid_fields[key] = raw_field

                        col_count += 1
                    else:
                        nc_key += field_shift
                        col_count = 2
                        row_even = True

                        if nc_key in conf.grid.fields_iso:
                            pass
                        else:
                            break

                        if field_data.sprite_index != 2:
                            image = self.sprite_sheet_handler.image_by_index(field_data.sprite_sheet, field_data.sprite_index)
                            field = Field(self.world.grid.fields_iso[nc_key].rect.topleft, image)
                            field.sprite_sheet_id = field_data.sprite_sheet
                            field.sprite_id = field_data.sprite_index
                            field.solid = field_data.solid
                            field.iso_key = nc_key
                            field.temperature = temperature

                            raw_field = RawField()
                            raw_field.rect = self.world.grid.fields_iso[nc_key].rect
                            raw_field.iso_key = field.iso_key
                            raw_field.sprite_sheet = field_data.sprite_sheet
                            raw_field.sprite_index = field_data.sprite_index
                            raw_field.temperature = temperature
                            if 2 < field_data.sprite_index < 5:
                                raw_field.solid = True
                                field.solid = True
                            else:
                                raw_field.solid = False
                                field.solid = False

                            self.fields.add(field)
                            self.world.grid_fields[key] = raw_field
                nc_key += 1

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
                    self.world.entities.add(tree)

    # todo: refactor save and load functions
    def load_fields_by_dict(self, fields_data: dict) -> None:
        pass

    # todo: refactor save and load functions
    def load_trees_by_dict(self, trees_data: dict) -> None:
        pass
