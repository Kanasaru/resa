""" This module provides classes to load world

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
import pygame.sprite
from data.world.entities.tree import RawTree
from data.world.generator import Generator
from data.world.objects.field import RawField
import data.eventcodes as ecodes


class Moving(object):
    def __init__(self) -> None:
        """ Dataclass for map movement """
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def __bool__(self) -> bool:
        """ Checks for any movement

        :return: True if any movement is active
        """
        if self.up or self.down or self.left or self.right:
            return True

        return False


class Map(object):
    def __init__(self, screen_size: tuple[int, int]) -> None:
        """ Initializes a world loading instance

        :param screen_size: tuple of screen size
        """
        # event handling varibales
        self.moving = Moving()

        # surfaces
        self.screen_size = screen_size
        self.surface = pygame.Surface(self.screen_size)
        self.bg_surface = pygame.Surface(self.screen_size)

        # world data
        self.rect = pygame.Rect((0, 0), (0, 0))
        self.water = pygame.sprite.Group()
        self.fields = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()

    def get_raw_fields(self) -> list:
        """ Returns basic information of all fields

        :return: list of raw fields
        """
        raw_fields = []
        for field in self.fields:
            raw_field = RawField()
            raw_field.pos = field.position
            raw_field.sprite_index = field.sprite_id
            raw_field.sprite_sheet = field.sprite_sheet_id
            raw_field.solid = field.solid
            raw_fields.append(raw_field)

        return raw_fields

    def get_raw_trees(self) -> list:
        """ Returns basic information of all trees

        :return: list of raw trees
        """
        raw_trees = []
        for tree in self.trees:
            raw_tree = RawTree()
            raw_tree.pos = tree.position
            raw_tree.sprite_index = tree.sprite_id
            raw_tree.sprite_sheet = tree.sprite_sheet_id
            raw_trees.append(raw_tree)

        return raw_trees

    def handle_event(self, event: pygame.event.Event) -> None:
        """ Handles given event

        :param event: pygame event
        :return: None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving.left = True
            if event.key == pygame.K_RIGHT:
                self.moving.right = True
            if event.key == pygame.K_UP:
                self.moving.up = True
            if event.key == pygame.K_DOWN:
                self.moving.down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving.left = False
            if event.key == pygame.K_RIGHT:
                self.moving.right = False
            if event.key == pygame.K_UP:
                self.moving.up = False
            if event.key == pygame.K_DOWN:
                self.moving.down = False
        else:
            pass

        self.fields.update(event)
        self.trees.update(event)

    def build_world(self, world_data: tuple[pygame.Rect, dict, dict] = None) -> None:
        """ Builds the world from scratch or given world data

        :param world_data: world data from game data handler
        :return: None
        """
        world = Generator()

        if world_data is not None:
            rect, field_data, tree_data = world_data
            # set basic world generation value from given data
            world.rect = rect
            world.size = rect.size
            # fill world with water and set fields and trees from given data
            world.fill()
            world.load_fields_by_dict(field_data)
            world.load_trees_by_dict(tree_data)
        else:
            # create a new world from scratch
            world.create()

        # get all sprites from world
        self.water, self.fields, self.trees, self.rect = world.get_world()
        # move the water sprites to avoid topleft isometric black fields
        self.water.update(pygame.event.Event(ecodes.RESA_GAME_EVENT,
                                             code=ecodes.RESA_CTRL_MAP_MOVE,
                                             move=(-50, -50)))
        # draw water sprites to its own surface
        self.water.draw(self.bg_surface)

    def run_logic(self) -> None:
        """ Runs the logic for the loaded world

        :return: None
        """
        if self.moving:
            # detect amount of movable space in each direction
            movable_px_right = self.rect.width - self.screen_size[0] - abs(0 - self.rect.x) + conf.grid.width / 2
            movable_px_left = abs(0 - self.rect.x)
            movable_px_up = abs(0 - self.rect.y)
            movable_px_down = self.rect.height - self.screen_size[1] - abs(0 - self.rect.y)

            # create and fill movement
            move_field = (0, 0)
            if self.moving.left and movable_px_left != 0:
                if movable_px_left < conf.map_pace:
                    self.rect.x += movable_px_left
                    move_field = (movable_px_left, 0)
                else:
                    self.rect.x += conf.map_pace
                    move_field = (conf.map_pace, 0)
            elif self.moving.right and movable_px_right != 0:
                if movable_px_right < conf.map_pace:
                    self.rect.x -= movable_px_right
                    move_field = (-movable_px_right, 0)
                else:
                    self.rect.x -= conf.map_pace
                    move_field = (-conf.map_pace, 0)
            if self.moving.up and movable_px_up != 0:
                if movable_px_up < conf.map_pace:
                    self.rect.y += movable_px_up
                    move_field = (move_field[0], movable_px_up)
                else:
                    self.rect.y += conf.map_pace
                    move_field = (move_field[0], conf.map_pace)
            elif self.moving.down and movable_px_down != 0:
                if movable_px_down < conf.map_pace:
                    self.rect.y -= movable_px_down
                    move_field = (move_field[0], -movable_px_down)
                else:
                    self.rect.y -= conf.map_pace
                    move_field = (move_field[0], -conf.map_pace)

            # raise event for movement
            pygame.event.post(pygame.event.Event(ecodes.RESA_GAME_EVENT,
                                                 code=ecodes.RESA_CTRL_MAP_MOVE,
                                                 move=move_field))

    def render(self) -> None:
        """ Renders all fields of the world on its surface

        :return: None
        """
        # render the background (water)
        self.surface.blit(self.bg_surface, (0, 0))

        # render all fields and trees
        self.fields.draw(self.surface)
        self.trees.draw(self.surface)

    def get_surface(self) -> pygame.Surface:
        """ Returns the current state of the map surface

        :return: current map surface
        """
        return self.surface
