class Grid(object):
    def __init__(self):
        # self.size has to be dividable by 2
        self.size = 20
        self.WIDTH = 6
        self.HEIGHT = 4

    def get_field_by_number(self, field_number):
        if field_number >= (self.WIDTH * self.HEIGHT):
            print("[ERR] field number is out of range")
            return False
        d = divmod(field_number, self.WIDTH)
        y = d[0] * self.size
        x = d[1] * self.size
        return x, y

    def get_field_by_pos(self, position):
        if position[0] >= (self.WIDTH * self.size):
            return False
        if position[1] >= (self.HEIGHT * self.size):
            return False
        d = divmod(position[0], self.size)
        x = d[0] * self.size
        d = divmod(position[1], self.size)
        y = d[0] * self.size
        return x, y

    def get_field_nr(self, position):
        position = self.get_field_by_pos(position)
        row = position[1] / self.size
        x = divmod(position[0], self.size)
        if row == 0:
            return 1 + x[0]
        return int(row * self.WIDTH + x[0] + 1)

    def get_grid_size(self):
        x: int = self.WIDTH
        y: int = self.HEIGHT
        return x, y

    def get_field_size(self):
        return self.size
