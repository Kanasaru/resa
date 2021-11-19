""" This module provides grid handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

__version__ = '1.0'


class Grid(object):
    def __init__(self, size: tuple[int, int]) -> None:
        """ Initializes a grid

        :param size: dimension of the grid
        """
        self.size = size[0]
        self.WIDTH = size[1]
        self.HEIGHT = size[2]

    def get_field_by_number(self, field_number: int) -> tuple[int, int] | bool:
        """ Returns a field in the grid by its number

        :param field_number:
        :return: field if found or false
        """
        if field_number >= (self.WIDTH * self.HEIGHT):
            print("[ERR] field number is out of range")
            return False
        d = divmod(field_number, self.WIDTH)
        y = d[0] * self.size
        x = d[1] * self.size
        return x, y

    def get_field_by_pos(self, position: tuple[int, int]) -> tuple[int, int] | bool:
        """ Returns a field in the grid by its position

        :param position:
        :return: field if found or false
        """
        if position[0] >= (self.WIDTH * self.size):
            return False
        if position[1] >= (self.HEIGHT * self.size):
            return False
        d = divmod(position[0], self.size)
        x = d[0] * self.size
        d = divmod(position[1], self.size)
        y = d[0] * self.size
        return x, y

    def get_field_nr(self, position: tuple[int, int]) -> int:
        """ Searches for a field by given position and return its field number if found

        :param position: position of field in grid to search for
        :return: field number in grid
        """
        position = self.get_field_by_pos(position)
        row = position[1] / self.size
        x = divmod(position[0], self.size)
        if row == 0:
            return x[0]
        return int(row * self.WIDTH + x[0])

    def get_grid_size(self) -> tuple[int, int]:
        """ Returns the dimension of the grid

        :return: grid size in number of fields
        """
        x: int = self.WIDTH
        y: int = self.HEIGHT
        return x, y

    def get_field_size(self) -> int:
        """ returns the dimension of the fields in the grid

        :return: grid field size in pixel
        """
        return self.size

    def get_grid_width_in_px(self) -> int:
        """ Returns the gird with in pixel

        :return: grid width in pixel
        """
        return self.WIDTH * self.size

    def get_grid_height_in_px(self) -> int:
        """ Returns the grid height in pixel

        :return: grid height in pixel
        """
        return self.HEIGHT * self.size

    def get_size(self) -> tuple[int, int]:
        """ Returns the grid size in pixel

        :return: grid size in pixel
        """
        x: int = self.WIDTH * self.size
        y: int = self.HEIGHT * self.size
        return x, y
