""" This module provides classes to create a normal and an isometric grid

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame


class GridField(object):
    def __init__(self, key: int, left: int, top: int, width: int, height: int, col: int, row: int):
        """ Contains information of a single field in a grid.

        :param key: field number in the grid
        :param left: position on the x-axis
        :param top: position on the y-axis
        :param width: with of the single field
        :param height: height of the single field
        :param col: optional grid col number
        :param row: optional grid row number
        """
        self.key = key
        self.col = col
        self.row = row
        self.rect = pygame.Rect((left, top), (width, height))

    def __str__(self):
        return f'Field {self.key}: {self.rect.topleft}, {self.rect.size}, Col: {self.col} Row: {self.row}'


class Grid(object):
    def __init__(self, fields_x: int, fields_y: int, grid: int):
        """ Creates a normal and isometric grid.
            fields_x has to be divisible by 2

        :param fields_x: number of fields on x-axis
        :param fields_y: number of fields on y-axis
        :param grid: size for the sides of a grid field
        """
        # basic grid information
        self.fields_x = int(fields_x)
        self.fields_y = int(fields_y)
        self.width = int(grid)
        self.height = int(grid)
        self.iso_width = self.width * 2
        self.iso_height = self.height

        # calculate the width and height of the grid
        self.grid_width = self.fields_x * self.width
        self.grid_height = self.fields_y * self.height

        # grid field dictionaries
        self.fields = dict()
        self.fields_iso = dict()

        # calculate the grids
        self.calc_grid()
        self.calc_iso_grid()

    def calc_grid(self) -> None:
        """ Calculates the normal grid and fills the grid field dictionary.

        :return: None
        """
        key = 1
        for row in range(self.fields_y):
            for col in range(self.fields_x):
                x = col * self.width
                y = row * self.height
                self.fields[key] = GridField(key, x, y, self.width, self.height, col, row)
                key += 1

    def draw_grid(self, surface: pygame.Surface,
                  position: tuple[int, int] = (0, 0),
                  color: tuple[int, int, int] = (255, 0, 0)) -> None:
        """ Draws the normal grid onto given surface.

        :param surface: surface on which the grid is drawn
        :param position: position in surface
        :param color: color of the grid
        :return: None
        """
        for key, value in self.fields.items():
            rect = pygame.Rect((value.rect.x + position[0], value.rect.y + position[1]), (self.width, self.height))
            pygame.draw.rect(surface, color, rect, 1)

    def pos_in_grid_field(self, point: tuple[int, int]) -> GridField | bool:
        """ Checks if given position is in grid and return the grid field as GridField.
            Given point is checked against a grid with a position on (0, 0). Point has to be normalized.

        :param point: point that has to be checked
        :return: False if point is not in grid or GridField if point is in grid
        """
        pos_div_x = divmod(point[0], self.width)
        pos_div_y = divmod(point[1], self.height)
        row = pos_div_y[0]
        col = pos_div_x[0]

        if row >= self.fields_y or col >= self.fields_x:
            return False

        key = row * self.fields_x + col + 1

        return self.fields[key]

    def calc_iso_grid(self) -> None:
        """ Calculates the isometric grid and fills the isometric grid field dictionary.

        :return: None
        """
        key = 1
        y = row = 0

        for row_nb in range(self.fields_y):
            for col_nb in range(self.fields_x // 2):
                x = (self.iso_width // 2 + col_nb * self.iso_width) - self.width
                y = self.iso_height * row_nb

                self.fields_iso[key] = GridField(key, x, y, self.iso_width, self.iso_height, col_nb, row)
                key += 1

            # go through half lines
            if row_nb < self.fields_y - 1:
                row += 1
                col = 0
                x = -self.width
                y += self.iso_height // 2
                for halfline in range(self.fields_x // 2 - 1):
                    x += self.iso_width
                    self.fields_iso[key] = GridField(key, x, y, self.iso_width, self.iso_height, col, row)
                    key += 1
                    col += 1
            row += 1

    def draw_iso_grid(self, surface: pygame.Surface,
                      position: tuple[int, int] = (0, 0),
                      color: tuple[int, int, int] = (0, 255, 0)) -> None:
        """ Draws the isometric grid onto given surface.

        :param surface: surface on which the grid is drawn
        :param position: position in surface
        :param color: color of the grid
        :return: None
        """
        for row_nb in range(self.fields_y):
            for col_nb in range(self.fields_x // 2):
                # calculate the isometric corners
                pos_left_x = position[0] + int((col_nb * self.iso_width))
                pos_left_y = position[1] + int((self.iso_height // 2) * (row_nb * 2 + 1))
                pos_top_x = position[0] + int((self.iso_width / 2 + col_nb * self.iso_width))
                pos_top_y = position[1] + int(self.iso_height * row_nb)
                pos_right_x = position[0] + int((col_nb + 1) * self.iso_width)
                pos_right_y = position[1] + int((self.iso_height // 2) * (row_nb * 2 + 1))
                pos_bottom_x = position[0] + int((self.iso_width / 2 + col_nb * self.iso_width))
                pos_bottom_y = position[1] + int(self.iso_height * (row_nb + 1))

                # calculate the starting and ending points of the corners
                line_left_top_start = (pos_left_x, pos_left_y - 1)
                line_left_top_end = (pos_top_x - 1, pos_top_y)
                line_top_right_start = (pos_top_x, pos_top_y)
                line_top_right_end = (pos_right_x - 1, pos_right_y - 1)
                line_left_bottom_start = (pos_left_x, pos_left_y)
                line_left_bottom_end = (pos_bottom_x - 1, pos_bottom_y - 1)
                line_bottom_right_start = (pos_bottom_x, pos_bottom_y - 1)
                line_bottom_right_end = (pos_right_x - 1, pos_right_y)

                # draw the isometric field
                pygame.draw.line(surface, color, line_left_top_start, line_left_top_end)
                pygame.draw.line(surface, color, line_top_right_start, line_top_right_end)
                pygame.draw.line(surface, color, line_left_bottom_start, line_left_bottom_end)
                pygame.draw.line(surface, color, line_bottom_right_start, line_bottom_right_end)

    def pos_in_iso_grid_field(self, point: tuple[int, int]) -> GridField | bool:
        """ Checks if given position is in isometric grid and return the grid field as GridField.
            Given point is checked against a grid with a position on (0, 0). Point has to be normalized.

        :param point: point that has to be checked
        :return: False if point is not in grid or GridField if point is in grid
        """
        pos_x = point[0]
        pos_y = point[1]

        if pos_x > self.grid_width or pos_y > self.grid_height:
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

        # possible field keys
        iso_col = divmod(col, 2)
        iso_key = iso_col[0] + row * self.fields_x // 2 + (row * (self.fields_x // 2 - 1)) + 1
        iso_key_top_left = iso_col[0] + (row - 1) * self.fields_x // 2 + (row * (self.fields_x // 2 - 1)) + 1
        iso_key_top_right = iso_col[0] + (row - 1) * self.fields_x // 2 + (row * (self.fields_x // 2 - 1)) + 2
        iso_key_bottom_left = iso_col[0] + (row + 1) * self.fields_x // 2 + (row * (self.fields_x // 2 - 1))
        iso_key_bottom_right = iso_col[0] + (row + 1) * self.fields_x // 2 + (row * (self.fields_x // 2 - 1)) + 1

        # detect correct key by checking point in triangles
        if col % 2 == 0:
            if Grid.is_in_triangle(x1, y1, x2, y2, x3_1, y3, pos_x, pos_y):
                if pos_x < self.iso_width // 2 or pos_y < self.iso_height // 2:
                    return False
                iso_key = iso_key_top_left
            elif Grid.is_in_triangle(x3_1, y3 + 1, x4, y4, x5, y5, pos_x, pos_y):
                if pos_x < self.iso_width // 2 or (self.grid_height - pos_y) < self.iso_height // 2:
                    return False
                iso_key = iso_key_bottom_left
        else:
            if Grid.is_in_triangle(x1, y1, x2, y2, x3_2, y3, pos_x, pos_y):
                if (self.grid_width - pos_x) < self.iso_width // 2 or pos_y < self.iso_height // 2:
                    return False
                iso_key = iso_key_top_right
            elif Grid.is_in_triangle(x3_2, y3 + 1, x4, y4, x5, y5, pos_x, pos_y):
                if (self.grid_width - pos_x) < self.iso_width // 2 or (self.grid_height - pos_y) < self.iso_height // 2:
                    return False
                iso_key = iso_key_bottom_right

        return self.fields_iso[iso_key]

    @staticmethod
    def area_of_triangle(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> float:
        """ Calculates the area of a triangle.

        :param x1: x of point 1
        :param y1: y of point 1
        :param x2: x of point 2
        :param y2: y of point 2
        :param x3: x of point 3
        :param y3: y of point 3
        :return: area of the triangle
        """
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

    @staticmethod
    def is_in_triangle(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x: float, y: float) -> bool:
        """ Checks if a point is in a triangle, which is created by given points.

        :param x1: x of point 1
        :param y1: y of point 1
        :param x2: x of point 2
        :param y2: y of point 2
        :param x3: x of point 3
        :param y3: y of point 3
        :param x: x of checked point
        :param y: y of checked point
        :return: true if point is in triangle or false if not.
        """
        area = Grid.area_of_triangle(x1, y1, x2, y2, x3, y3)
        area_1 = Grid.area_of_triangle(x, y, x2, y2, x3, y3)
        area_2 = Grid.area_of_triangle(x1, y1, x, y, x3, y3)
        area_3 = Grid.area_of_triangle(x1, y1, x2, y2, x, y)

        if area == area_1 + area_2 + area_3:
            return True

        return False
