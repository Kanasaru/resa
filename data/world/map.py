import pygame.sprite
import data.helpers.spritesheet
from data import settings
from data.world import fields
from data.world.islands import big_islands


class Field(pygame.sprite.Sprite):
    def __init__(self, position: tuple, size: tuple, image: pygame.image) -> None:
        """
        :param position: position on world surface
        :param size: field size
        :param image: field image
        """
        pygame.sprite.Sprite.__init__(self)

        self.pos = position
        self.image = image
        self.size = size

        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self) -> None:
        self.rect.topleft = self.pos

    def position(self, position: tuple = None) -> tuple | bool:
        if position is not None:
            self.pos = position
            return True
        return self.pos

    def move(self, movement: tuple) -> None:
        pos_x = self.pos[0] + movement[0]
        pox_y = self.pos[1] + movement[1]
        self.pos = (pos_x, pox_y)

    def delete(self):
        self.kill()


class Loader(object):
    def __init__(self, size: tuple, grid_size: tuple) -> None:
        """
        :param size: tuple of screen size
        :param spritesheet: path to spritesheet
        :param grid_size: tuple of single grid (field) size
        :param sprite_size: tuple of single sprite size in spritesheet
        :param colorkey: rgb tuple of used colorkey in spritesheet
        """
        self.size = size
        self.grid_size = grid_size
        self.fields = pygame.sprite.Group()
        self.sprite_sheets = []
        self.field_data = fields.FIELD_DICT
        self.rect = pygame.Rect(settings.WORLD_START_POS,
                                (settings.WORLD_SIZE[0]*self.grid_size[0], settings.WORLD_SIZE[1]*self.grid_size[1]))

        for sheet in fields.SPRITE_SHEETS:
            self.sprite_sheets.append(data.helpers.spritesheet.SpriteSheet(fields.SPRITE_SHEETS[sheet]))

        self.surface = pygame.Surface(self.size)
        self.surface.fill(settings.COLOR_BLACK)

        self.map_pace = settings.MAP_PACE
        self.moving = False
        self.move_steps = (0, 0)

        self.load_fields()

    def handle_event(self, event) -> None:
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

    def render(self):
        self.surface.fill(settings.COLOR_BLACK)
        self.fields.draw(self.surface)

    def load_fields(self):
        # load water
        pos_x = 20
        pos_y = 0
        for row in range(settings.WORLD_SIZE[1] * 2 - 1):
            for col in range(settings.WORLD_SIZE[0]):
                image = self.sprite_sheets[fields.FIELD_DICT[5]["sprite_sheet"]].image_at(
                    fields.FIELD_DICT[5]["sprite_rect"],
                    fields.FIELD_DICT[5]["colorkey"]
                )
                self.fields.add(Field((pos_x, pos_y), self.grid_size, image))
                pos_x += self.grid_size[0]
            pos_y += self.grid_size[1] / 2
            if (row % 2) == 0:
                pos_x = 0
            else:
                pos_x = self.grid_size[0] / 2

        # load islands
        self.load_island((7, 6))

    def get_surface(self):
        return self.surface

    def load_island(self, position):
        offset = divmod(len(big_islands.big_island_one), 2)
        start_x = (position[0] + offset[0] + 1) * self.grid_size[0]
        start_y = position[1] * self.grid_size[1] - self.grid_size[1] / 2

        for row_nb, row in enumerate(big_islands.big_island_one):
            for col_nb, tile in enumerate(row):
                if tile == 0:
                    pass
                else:
                    neighbors = [
                        big_islands.big_island_one[row_nb][col_nb - 1],  # left
                        big_islands.big_island_one[row_nb][col_nb + 1],  # right
                        big_islands.big_island_one[row_nb - 1][col_nb],  # top
                        big_islands.big_island_one[row_nb + 1][col_nb],  # bottom
                        big_islands.big_island_one[row_nb - 1][col_nb - 1],  # corner top left
                        big_islands.big_island_one[row_nb - 1][col_nb + 1],  # corner top right
                        big_islands.big_island_one[row_nb + 1][col_nb - 1],  # corner bottom left
                        big_islands.big_island_one[row_nb + 1][col_nb + 1],  # corner bottom right
                    ]
                    # sides
                    if neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1:
                        identifier = 30
                    elif neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 1:
                        identifier = 31
                    elif neighbors[0] == 1 and neighbors[1] == 0 and neighbors[2] == 1 and neighbors[3] == 1:
                        identifier = 32
                    elif neighbors[0] == 1 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 0:
                        identifier = 33
                    # inner corner
                    elif neighbors[0] == 1 and neighbors[1] == 0 and neighbors[2] == 1 and neighbors[3] == 0:
                        identifier = 6
                    elif neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 0 and neighbors[3] == 1:
                        identifier = 7
                    elif neighbors[0] == 1 and neighbors[1] == 0 and neighbors[2] == 0 and neighbors[3] == 1:
                        identifier = 8
                    elif neighbors[0] == 0 and neighbors[1] == 1 and neighbors[2] == 1 and neighbors[3] == 0:
                        identifier = 9
                    # inner corner side
                    elif neighbors[7] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
                        identifier = 22
                    elif neighbors[4] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
                        identifier = 23
                    elif neighbors[6] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
                        identifier = 24
                    elif neighbors[5] == 0 and neighbors[0] == 1 and neighbors[2] == 1:
                        identifier = 25
                    else:
                        identifier = 1
                    cart_x = row_nb * (self.grid_size[0] / 2)
                    cart_y = col_nb * self.grid_size[1]
                    pos_x = (cart_x - cart_y)
                    pos_y = (cart_x + cart_y) / 2
                    image = self.sprite_sheets[fields.FIELD_DICT[identifier]["sprite_sheet"]].image_at(
                        fields.FIELD_DICT[identifier]["sprite_rect"],
                        fields.FIELD_DICT[identifier]["colorkey"]
                    )
                    for field in self.fields:
                        if field.position() == (start_x + pos_x, start_y + pos_y):
                            field.delete()
                    self.fields.add(Field((start_x + pos_x, start_y + pos_y), self.grid_size, image))
