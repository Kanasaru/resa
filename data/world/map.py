""" This module provides classes to load world

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

import pygame.sprite
import data.helpers.color as colors
from data import settings
from data.world import fields
from data.world.generator import Generator


class Loader(object):
    def __init__(self, size: tuple[int, int], grid_size: tuple[int, int]) -> None:
        """ Initializes a world loading instance

        :param size: tuple of screen size
        :param grid_size: tuple of single grid (field) size
        """
        self.size = size
        self.grid_size = grid_size
        self.surface = pygame.Surface(self.size)
        self.surface.fill(colors.COLOR_BLACK)
        self.map_pace = settings.MAP_PACE
        self.moving = False
        self.move_steps = (False, False, False, False)
        self.fields = None
        self.rect = None

    def get_fields(self):
        return self.fields

    def get_raw_fields(self):
        raw_fields = []
        for field in self.fields:
            raw_fields.append([field.position(), (field.sprite_sheet_id, field.sprite_id), field.solid])
        return raw_fields

    def get_rect(self):
        return self.rect

    def handle_event(self, event) -> None:
        """ Handles given event

        :param event: pygame or resa event object
        :return: None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_steps_l = True
            else:
                move_steps_l = self.move_steps[0]
            if event.key == pygame.K_RIGHT:
                move_steps_r = True
            else:
                move_steps_r = self.move_steps[1]
            if event.key == pygame.K_UP:
                move_steps_u = True
            else:
                move_steps_u = self.move_steps[2]
            if event.key == pygame.K_DOWN:
                move_steps_d = True
            else:
                move_steps_d = self.move_steps[3]
            self.move_steps = (move_steps_l, move_steps_r, move_steps_u, move_steps_d)
            if self.move_steps[0] or self.move_steps[1] or self.move_steps[2] or self.move_steps[3]:
                self.moving = True
            else:
                self.moving = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_steps_l = False
            else:
                move_steps_l = self.move_steps[0]
            if event.key == pygame.K_RIGHT:
                move_steps_r = False
            else:
                move_steps_r = self.move_steps[1]
            if event.key == pygame.K_UP:
                move_steps_u = False
            else:
                move_steps_u = self.move_steps[2]
            if event.key == pygame.K_DOWN:
                move_steps_d = False
            else:
                move_steps_d = self.move_steps[3]
            self.move_steps = (move_steps_l, move_steps_r, move_steps_u, move_steps_d)
            if self.move_steps[0] or self.move_steps[1] or self.move_steps[2] or self.move_steps[3]:
                self.moving = True
            else:
                self.moving = False
        else:
            pass

    def build_world(self, world_data: tuple[pygame.Rect, dict] = None):
        if world_data is not None:
            rect, field_data = world_data
            world = Generator(rect.size, self.grid_size)
            for sheet in fields.SPRITE_SHEETS:
                world.add_sprite_sheet(fields.SPRITE_SHEETS[sheet])
            world.set_field_dict(fields.FIELD_DICT)
            world.load_fields_by_dict(field_data)
            world.rect = rect
        else:
            world = Generator(settings.WORLD_SIZE, self.grid_size)
            for sheet in fields.SPRITE_SHEETS:
                world.add_sprite_sheet(fields.SPRITE_SHEETS[sheet])
            world.set_field_dict(fields.FIELD_DICT)
            world.fill(5)
            # todo: using random island method
            world.add_island((-2, 2))

        self.fields, self.rect = world.get_world()

    def run_logic(self) -> None:
        """ Runs the logic for the loaded world

        :return: None
        """
        if self.moving:
            movable_px_right = self.rect.width - self.size[0] - abs(0 - self.rect.x) + self.grid_size[0] / 2
            movable_px_left = abs(0 - self.rect.x)
            movable_px_up = abs(0 - self.rect.y)
            movable_px_down = self.rect.height - self.size[1] - abs(0 - self.rect.y)
            move_field = (0, 0)
            # move left
            if self.move_steps[0] and movable_px_left != 0:
                if movable_px_left < self.map_pace:
                    self.rect.x += movable_px_left
                    move_field = (movable_px_left, 0)
                else:
                    self.rect.x += self.map_pace
                    move_field = (self.map_pace, 0)
            # move right
            elif self.move_steps[1] and movable_px_right != 0:
                if movable_px_right < self.map_pace:
                    self.rect.x -= movable_px_right
                    move_field = (-movable_px_right, 0)
                else:
                    self.rect.x -= self.map_pace
                    move_field = (-self.map_pace, 0)
            # move up
            if self.move_steps[2] and movable_px_up != 0:
                if movable_px_up < self.map_pace:
                    self.rect.y += movable_px_up
                    move_field = (move_field[0], movable_px_up)
                else:
                    self.rect.y += self.map_pace
                    move_field = (move_field[0], self.map_pace)
            # move down
            elif self.move_steps[3] and movable_px_down != 0:
                if movable_px_down < self.map_pace:
                    self.rect.y -= movable_px_down
                    move_field = (move_field[0], -movable_px_down)
                else:
                    self.rect.y -= self.map_pace
                    move_field = (move_field[0], -self.map_pace)
            # move layer
            for field in self.fields:
                field.move(move_field)

        self.fields.update()

    def render(self) -> None:
        """ Renders all fields of the world on its surface

        :return: None
        """
        self.surface.fill(colors.COLOR_BLACK)
        self.fields.draw(self.surface)

    def get_surface(self) -> pygame.Surface:
        """ Returns the current state of the world surface

        :return: current world surface
        """
        return self.surface

    def __bool__(self):
        if isinstance(self.fields, pygame.sprite.Group) and \
                len(self.fields) > 0 and \
                isinstance(self.rect, pygame.Rect):
            return True
        return False
