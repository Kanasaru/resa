""" This module provides classes to load world

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '0.2'

import pygame.sprite
from data import settings
from data.world import fields
from data.world.islands import big_islands
from data.world.generator import Generator


class Loader(object):
    def __init__(self, size: tuple[int, int], grid_size: tuple[int, int]) -> None:
        """ Initializes a world loading instance

        :param size: tuple of screen size
        :param grid_size: tuple of single grid (field) size
        """
        self.size = size
        self.grid_size = grid_size

        self.world = Generator(settings.WORLD_SIZE, grid_size)
        for sheet in fields.SPRITE_SHEETS:
            self.world.add_sprite_sheet(fields.SPRITE_SHEETS[sheet])
        self.world.set_field_dict(fields.FIELD_DICT)
        self.world.fill(5)
        self.world.add_island((0, 0), big_islands.big_island_one)
        self.world.add_island((10, 3), big_islands.big_island_two)

        self.fields, self.rect = self.world.get_world()

        self.surface = pygame.Surface(self.size)
        self.surface.fill(settings.COLOR_BLACK)

        self.map_pace = settings.MAP_PACE
        self.moving = False
        self.move_steps = (0, 0)

    def handle_event(self, event) -> None:
        """ Handles given event

        :param event: pygame or resa event object
        :return: None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_steps = (-self.map_pace, self.move_steps[1])
            if event.key == pygame.K_RIGHT:
                self.move_steps = (self.map_pace, self.move_steps[1])
            if event.key == pygame.K_UP:
                self.move_steps = (self.move_steps[0], -self.map_pace)
            if event.key == pygame.K_DOWN:
                self.move_steps = (self.move_steps[0], self.map_pace)
            self.moving = True
        elif event.type == pygame.KEYUP:
            self.moving = False
            self.move_steps = (0, 0)
        else:
            pass

    def run_logic(self) -> None:
        """ Runs the logic for the loaded world

        :return: None
        """
        new_pos_x = self.rect.x + self.move_steps[0]
        new_pos_y = self.rect.y + self.move_steps[1]

        if new_pos_x > 0:
            self.move_steps = (0, self.move_steps[1])
        elif (new_pos_x * -1 + self.size[0] - self.grid_size[0] / 2) >= self.rect.width:
            self.move_steps = (0, self.move_steps[1])
        else:
            self.rect.x = new_pos_x
        if new_pos_y > 0:
            self.move_steps = (self.move_steps[0], 0)
        elif (new_pos_y * -1 + self.size[1] - self.grid_size[1] / 2) >= self.rect.height:
            self.move_steps = (self.move_steps[0], 0)
        else:
            self.rect.y = new_pos_y

        for field in self.fields:
            field.move(self.move_steps)

        self.fields.update()

    def render(self) -> None:
        """ Renders all fields of the world on its surface

        :return: None
        """
        self.surface.fill(settings.COLOR_BLACK)
        self.fields.draw(self.surface)

    def get_surface(self) -> pygame.Surface:
        """ Returns the current state of the world surface

        :return: current world surface
        """
        return self.surface

