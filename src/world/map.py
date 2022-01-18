""" This module provides classes to load world

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame.sprite
from src.world.generator import Generator
from src.world.objects.field import Field
from src.handler import RESA_CH, RESA_SSH, RESA_GSH, RESA_EH


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
    def __init__(self, screen_size: tuple[int, int], map_shift: tuple[int, int]) -> None:
        """ Initializes a world loading instance

        :param screen_size: tuple of screen size
        """
        # event handling varibales
        self.moving = Moving()
        self.map_shift = map_shift

        self.buildsprites = pygame.sprite.Group()

        # surfaces
        self.screen_size = screen_size
        self.surface = pygame.Surface(self.screen_size)

        # world src
        self.rect = pygame.Rect((0, 0), (0, 0))

        self.world = None
        self.grid_image = None
        self.show_grid = False

    def build_world(self, world_data: tuple[pygame.Rect, dict, dict] = None) -> None:
        """ Builds the world from scratch or given world src

        :param world_data: world src from game src handler
        :return: None
        """
        world = Generator()

        if world_data is not None:
            rect, field_data, tree_data = world_data
            # set basic world generation value from given src
            world.rect = rect
            world.size = rect.size
            # fill world with water and set fields and trees from given src
            world.fill()
        else:
            # create a new world from scratch
            world.create()

        # get all sprites from world
        self.world = world.get_world()
        self.rect = self.world.rect
        # mouse shift for events
        self.world.mouse_shift_x = self.rect.x + self.map_shift[0]
        self.world.mouse_shift_y = self.rect.y + self.map_shift[1]

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
            if event.key == pygame.K_F5:
                self.show_grid = not self.show_grid
            # >>> BUILDMODE: just for testing
            if event.key == pygame.K_F6:
                RESA_GSH.building = not RESA_GSH.building
            if event.key == pygame.K_1:
                if RESA_GSH.building:
                    RESA_GSH.building_size = (1, 1)
            if event.key == pygame.K_2:
                if RESA_GSH.building:
                    RESA_GSH.building_size = (2, 2)
            if event.key == pygame.K_3:
                if RESA_GSH.building:
                    RESA_GSH.building_size = (3, 3)
            # <<<
        elif event.type == pygame.MOUSEMOTION and RESA_GSH.building:
            if self.map_shift[0] < event.pos[0] < self.surface.get_width() + self.map_shift[0] and \
                    self.map_shift[1] < event.pos[1] < self.surface.get_height() + self.map_shift[1]:
                self.draw_build_grid(event.pos, RESA_GSH.building_size)
            else:
                self.buildsprites.empty()
        else:
            pass

        self.world.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the logic for the loaded world

        :return: None
        """
        if self.moving:
            # detect amount of movable space in each direction
            movable_px_right = self.rect.width - self.screen_size[0] - abs(0 - self.rect.x)
            movable_px_left = abs(0 - self.rect.x)
            movable_px_up = abs(0 - self.rect.y)
            movable_px_down = self.rect.height - self.screen_size[1] - abs(0 - self.rect.y)

            # create and fill movement
            move_field = (0, 0)
            if self.moving.left and movable_px_left != 0:
                if movable_px_left < RESA_CH.map_pace:
                    self.rect.x += movable_px_left
                    move_field = (movable_px_left, 0)
                else:
                    self.rect.x += RESA_CH.map_pace
                    move_field = (RESA_CH.map_pace, 0)
            elif self.moving.right and movable_px_right != 0:
                if movable_px_right < RESA_CH.map_pace:
                    self.rect.x -= movable_px_right
                    move_field = (-movable_px_right, 0)
                else:
                    self.rect.x -= RESA_CH.map_pace
                    move_field = (-RESA_CH.map_pace, 0)
            if self.moving.up and movable_px_up != 0:
                if movable_px_up < RESA_CH.map_pace:
                    self.rect.y += movable_px_up
                    move_field = (move_field[0], movable_px_up)
                else:
                    self.rect.y += RESA_CH.map_pace
                    move_field = (move_field[0], RESA_CH.map_pace)
            elif self.moving.down and movable_px_down != 0:
                if movable_px_down < RESA_CH.map_pace:
                    self.rect.y -= movable_px_down
                    move_field = (move_field[0], -movable_px_down)
                else:
                    self.rect.y -= RESA_CH.map_pace
                    move_field = (move_field[0], -RESA_CH.map_pace)

            # raise event for movement
            pygame.event.post(
                pygame.event.Event(RESA_EH.RESA_GAME_EVENT, code=RESA_EH.RESA_CTRL_MAP_MOVE, move=move_field)
            )
            
        self.world.update()

    def render(self) -> None:
        """ Renders all fields of the world on its surface

        :return: None
        """
        self.surface.fill(RESA_CH.COLOR_BLACK)

        if self.show_grid:
            self.surface.blit(self.world.grid_image, self.rect.topleft)
        else:
            self.surface.blit(self.world.image, self.rect.topleft)

        if RESA_GSH.building:
            self.buildsprites.draw(self.surface)

        self.world.draw(self.surface)

    def get_surface(self) -> pygame.Surface:
        """ Returns the current state of the map surface

        :return: current map surface
        """
        return self.surface
    
    def draw_build_grid(self, position, size):
        x, y = size
        sprite_sheet = 'Tiles'
        # relativate to grid
        mouse_x = position[0] - self.rect.x - self.map_shift[0]
        mouse_y = position[1] - self.rect.y - self.map_shift[1]

        field = self.world.grid.pos_in_iso_grid_field((mouse_x, mouse_y))
        if field:
            neighbors = self.world.grid.iso_grid_neighbors(field.key)
            self.buildsprites.empty()
            # 1x1
            if x == y == 1:
                raw_field = self.world.grid_fields[field.key]
                if raw_field.buildable and not raw_field.building:
                    sprite_index = 1
                else:
                    sprite_index = 0
                image = RESA_SSH.image_by_index(sprite_sheet, sprite_index)
                new_field = Field((raw_field.rect.x, raw_field.rect.y), image)
                self.buildsprites.add(new_field)
            # 2x2
            elif x == y == 2:
                raw_field = self.world.grid_fields[field.key]
                if raw_field.buildable and not raw_field.building:
                    sprite_index = 1
                else:
                    sprite_index = 0
                image = RESA_SSH.image_by_index(sprite_sheet, sprite_index)
                new_field = Field((raw_field.rect.x, raw_field.rect.y), image)
                self.buildsprites.add(new_field)
                # set all neighbors false that are not used
                neighbors.left = -1
                neighbors.right = -1
                neighbors.bottom = -1
                neighbors.bottomleft = -1
                neighbors.bottomright = -1
                for rawval in neighbors.all:
                    if rawval:
                        raw_field = self.world.grid_fields[rawval]
                        if raw_field.buildable and not raw_field.building:
                            sprite_index = 1
                        else:
                            sprite_index = 0
                        image = RESA_SSH.image_by_index(sprite_sheet, sprite_index)
                        new_field = Field((raw_field.rect.x, raw_field.rect.y), image)
                        self.buildsprites.add(new_field)
            # 3x3
            elif x == y == 3:
                # get field and neighbors
                if field:
                    # add sprites
                    raw_field = self.world.grid_fields[field.key]
                    if raw_field.buildable and not raw_field.building:
                        sprite_index = 1
                    else:
                        sprite_index = 0
                    image = RESA_SSH.image_by_index(sprite_sheet, sprite_index)
                    new_field = Field((raw_field.rect.x, raw_field.rect.y), image)
                    self.buildsprites.add(new_field)
                    for rawval in neighbors.all:
                        if rawval:
                            raw_field = self.world.grid_fields[rawval]
                            if raw_field.buildable and not raw_field.building:
                                sprite_index = 1
                            else:
                                sprite_index = 0
                            image = RESA_SSH.image_by_index(sprite_sheet, sprite_index)
                            new_field = Field((raw_field.rect.x, raw_field.rect.y), image)
                            self.buildsprites.add(new_field)
