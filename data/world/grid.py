""" This module provides grid handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""

import logging
import pygame


class OldGrid(object):
    def __init__(self, size: tuple[tuple, int, int]) -> None:
        """ Initializes a grid
        :param size: dimension of the grid
        """
        self.size = (size[1], size[2])
        self.grid_width = int(size[0][0] / size[1])
        self.grid_height = int(size[0][1] / size[2])
        self.width = size[1]
        self.height = size[2]


class GridField(object):
    def __init__(self, key: int, left: int, top: int, width: int, height: int):
        self.key = key
        self.rect = pygame.Rect((left, top), (width, height))

    def __str__(self):
        return f'Field {self.key}: {self.rect.topleft}, {self.rect.size}'


class Grid(object):
    def __init__(self, fields_x: int, fields_y: int, width: int, height: int):
        self.fields_x = fields_x
        self.fields_y = fields_y
        self.width = width
        self.height = height
        self.iso_width = width * 2
        self.iso_height = height

        self.color_grid = (255, 0, 0)
        self.color_iso = (0, 255, 0)

        self.fields = dict()
        self.fields_iso = dict()

        self.calc_grid()
        self.calc_iso_grid()

    def calc_grid(self):
        key = 1
        for row in range(self.fields_y):
            for col in range(self.fields_x):
                x = col * self.width
                y = row * self.height
                self.fields[key] = GridField(key, x, y, self.width, self.height)
                key += 1

    def draw_grid(self, surface):
        for key, value in self.fields.items():
            pygame.draw.rect(surface, self.color_grid, value.rect, 1)

    def pos_in_grid_field(self, position):
        pos_div_x = divmod(position[0], self.width)
        pos_div_y = divmod(position[1], self.height)

        row = pos_div_y[0]
        col = pos_div_x[0]

        if row >= self.fields_y or col >= self.fields_x:
            logging.warning('Out of scope!')
            return False

        key = row * self.fields_x + col + 1

        return self.fields[key]

    def calc_iso_grid(self):
        key = 1
        buffer = (0, 0)

        for row_nb in range(self.fields_y):
            for col_nb in range(self.fields_x // 2):
                blx = int((self.iso_width / 2 + col_nb * self.iso_width)) - self.width - 2
                bly = int(self.iso_height * (row_nb + 1)) - self.iso_height
                buffer = 0, bly + self.height // 2

                self.fields_iso[key] = GridField(key, blx, bly, self.iso_width, self.iso_height)
                key += 1

            if row_nb < self.fields_y - 1:
                blpx, blpy = buffer
                for halfline in range(self.fields_x // 2 - 1):
                    blpx += self.width
                    self.fields_iso[key] = GridField(key, blpx, blpy, self.iso_width, self.iso_height)
                    key += 1

    def draw_iso_grid(self, surface):
        for row_nb in range(self.fields_y):
            for col_nb in range(self.fields_x // 2):
                pos_left_x = int((col_nb * self.iso_width))
                pos_left_y = int((self.iso_height // 2) * (row_nb * 2 + 1))
                pos_top_x = int((self.iso_width / 2 + col_nb * self.iso_width))
                pos_top_y = int(self.iso_height * row_nb)
                pos_right_x = int((col_nb + 1) * self.iso_width)
                pos_right_y = int((self.iso_height // 2) * (row_nb * 2 + 1))
                pos_bottom_x = int((self.iso_width / 2 + col_nb * self.iso_width))
                pos_bottom_y = int(self.iso_height * (row_nb + 1))

                line_left_top_start = (pos_left_x, pos_left_y - 1)
                line_left_top_end = (pos_top_x - 1, pos_top_y)
                line_top_right_start = (pos_top_x, pos_top_y)
                line_top_right_end = (pos_right_x - 1, pos_right_y - 1)
                line_left_bottom_start = (pos_left_x, pos_left_y)
                line_left_bottom_end = (pos_bottom_x - 1, pos_bottom_y - 1)
                line_bottom_right_start = (pos_bottom_x, pos_bottom_y - 1)
                line_bottom_right_end = (pos_right_x - 1, pos_right_y)

                pygame.draw.line(surface, self.color_iso, line_left_top_start, line_left_top_end)
                pygame.draw.line(surface, self.color_iso, line_top_right_start, line_top_right_end)
                pygame.draw.line(surface, self.color_iso, line_left_bottom_start, line_left_bottom_end)
                pygame.draw.line(surface, self.color_iso, line_bottom_right_start, line_bottom_right_end)

    def pos_in_iso_grid_field(self, position):
        pos_x = position[0]
        pos_y = position[1]
        max_width = (self.fields_x * self.iso_width) // 2
        max_height = self.fields_y * self.iso_height

        if pos_x > max_width or pos_y > max_height:
            logging.warning('Out of scope!')
            return False

        # calc grid row and col
        pos_div_x = divmod(pos_x, self.width)
        pos_div_y = divmod(pos_y, self.height)
        row = pos_div_y[0]
        col = pos_div_x[0]

        # field points
        x1 = col * self.iso_width // 2
        y1 = row * self.iso_height
        x2 = (col + 1) * self.iso_width // 2 - 1
        y2 = row * self.iso_height
        x3_1 = col * self.iso_width // 2
        x3_2 = (col + 1) * self.iso_width // 2
        y3 = (row + 1) * self.iso_height // 2 - 1 + (row * self.iso_height // 2)
        x4 = col * self.iso_width // 2
        y4 = (row + 1) * self.iso_height - 1
        x5 = (col + 1) * self.iso_width // 2 - 1
        y5 = (row + 1) * self.iso_height - 1

        # field key
        iso_col = divmod(col, 2)
        iso_field_key = iso_col[0] + row * self.fields_y + (row * (self.fields_y - 1)) + 1
        iso_field_key_top_left = iso_col[0] + (row - 1) * self.fields_y + (row * (self.fields_y - 1)) + 1
        iso_field_key_top_right = iso_col[0] + (row - 1) * self.fields_y + (row * (self.fields_y - 1)) + 2
        iso_field_key_bottom_left = iso_col[0] + (row + 1) * self.fields_y + (row * (self.fields_y - 1))
        iso_field_key_bottom_right = iso_col[0] + (row + 1) * self.fields_y + (row * (self.fields_y - 1)) + 1

        if col % 2 == 0:
            if Grid.is_point_in_triangle(x1, y1, x2, y2, x3_1, y3, pos_x, pos_y):
                if pos_x < self.iso_width // 2:
                    logging.warning('Out of scope!')
                    return False
                if pos_y < self.iso_height // 2:
                    logging.warning('Out of scope!')
                    return False
                iso_key = iso_field_key_top_left
                iso_x = x4 - self.width
                iso_y = y4 - self.height // 2 - self.iso_height + 1
            elif Grid.is_point_in_triangle(x3_1, y3 + 1, x4, y4, x5, y5, pos_x, pos_y):
                if pos_x < self.iso_width // 2:
                    logging.warning('Out of scope!')
                    return False
                if (max_height - pos_y) < self.iso_height // 2:
                    logging.warning('Out of scope!')
                    return False
                iso_key = iso_field_key_bottom_left
                iso_x = x4 - self.width
                iso_y = y4 + self.height // 2 - self.iso_height + 1
            else:
                iso_key = iso_field_key
                iso_x = x4
                iso_y = y4 - self.iso_height + 1
        else:
            if Grid.is_point_in_triangle(x1, y1, x2, y2, x3_2, y3, pos_x, pos_y):
                if (max_width - pos_x) < self.iso_width // 2:
                    logging.warning('Out of scope!')
                    return False
                if pos_y < self.iso_height // 2:
                    logging.warning('Out of scope!')
                    return False
                iso_key = iso_field_key_top_right
                iso_x = x4
                iso_y = y4 - self.height // 2 - self.iso_height + 1
            elif Grid.is_point_in_triangle(x3_2, y3 + 1, x4, y4, x5, y5, pos_x, pos_y):
                if (max_width - pos_x) < self.iso_width // 2:
                    logging.warning('Out of scope!')
                    return False
                if (max_height - pos_y) < self.iso_height // 2:
                    logging.warning('Out of scope!')
                    return False
                iso_key = iso_field_key_bottom_right
                iso_x = x4
                iso_y = y4 + self.height // 2 - self.iso_height + 1
            else:
                iso_key = iso_field_key
                iso_x = x4 - self.width
                iso_y = y4 - self.iso_height + 1

        return GridField(iso_key, iso_x, iso_y, self.iso_width, self.iso_height)

    @staticmethod
    def area_of_triangle(x1, y1, x2, y2, x3, y3):
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

    @staticmethod
    def is_point_in_triangle(x1, y1, x2, y2, x3, y3, x, y):
        area = Grid.area_of_triangle(x1, y1, x2, y2, x3, y3)
        area_1 = Grid.area_of_triangle(x, y, x2, y2, x3, y3)
        area_2 = Grid.area_of_triangle(x1, y1, x, y, x3, y3)
        area_3 = Grid.area_of_triangle(x1, y1, x2, y2, x, y)

        if area == area_1 + area_2 + area_3:
            return True

        return False
