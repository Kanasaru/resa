""" This module provides grid handling

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""


class Grid(object):
    def __init__(self, size: tuple[tuple, int, int]) -> None:
        """ Initializes a grid

        :param size: dimension of the grid
        """
        self.size = (size[1], size[2])
        self.grid_width = int(size[0][0] / size[1])
        self.grid_height = int(size[0][1] / size[2])
        self.width = size[1]
        self.height = size[2]

    def get_field_by_number(self, field_number: int) -> tuple[int, int] | bool:
        """ Returns a field in the grid by its number

        :param field_number:
        :return: field if found or false
        """
        if field_number >= (self.width * self.height):
            print("[ERR] field number is out of range")
            return False
        d = divmod(field_number, self.width)
        y = d[0] * self.grid_height
        x = d[1] * self.grid_width
        return x, y

    def get_field_by_pos(self, position: tuple[int, int]) -> tuple[int, int] | bool:
        """ Returns a field in the grid by its position

        :param position:
        :return: field if found or false
        """
        if position[0] >= (self.width * self.grid_width):
            return False
        if position[1] >= (self.height * self.grid_height):
            return False
        d = divmod(position[0], self.grid_width)
        x = d[0] * self.grid_width
        d = divmod(position[1], self.grid_height)
        y = d[0] * self.grid_height
        return x, y

    def get_field_nr(self, position: tuple[int, int]) -> int:
        """ Searches for a field by given position and return its field number if found

        :param position: position of field in grid to search for
        :return: field number in grid
        """
        position = self.get_field_by_pos(position)
        row = position[1] / self.grid_height
        x = divmod(position[0], self.grid_width)
        if row == 0:
            return x[0]
        return int(row * self.width + x[0])

    def get_grid_size(self) -> tuple[int, int]:
        """ Returns the dimension of the grid

        :return: grid size in number of fields
        """
        x: int = self.width
        y: int = self.height
        return x, y

    def get_field_size(self) -> tuple[int, int]:
        """ returns the dimension of the fields in the grid

        :return: grid field size in pixel
        """
        return self.grid_width, self.grid_height

    def get_grid_width_in_px(self) -> int:
        """ Returns the gird with in pixel

        :return: grid width in pixel
        """
        return self.width * self.grid_width

    def get_grid_height_in_px(self) -> int:
        """ Returns the grid height in pixel

        :return: grid height in pixel
        """
        return self.height * self.grid_height

    def get_size(self) -> tuple[int, int]:
        """ Returns the grid size in pixel

        :return: grid size in pixel
        """
        x: int = self.width * self.grid_width
        y: int = self.height * self.grid_height
        return x, y
