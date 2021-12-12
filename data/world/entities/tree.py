import pygame
from data.handlers.spritesheet import SpriteSheetHandler
from data.settings import conf


class RawTree(object):
    def __init__(self):
        self.pos = None
        self.sprite_index = None
        self.sprite_sheet = None
        self.solid = None


class Tree(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], image: pygame.image) -> None:
        pygame.sprite.Sprite.__init__(self)

        self._position = position
        self.image = image

        self.size = SpriteSheetHandler.aspect_ratio(self.image.get_rect().size, conf.grid.width)
        self.image = pygame.transform.scale(self.image, self.size).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.position

        self.sprite_sheet_id = None
        self.sprite_id = None
        self._growth = 3

    @property
    def growth(self):
        return self._growth

    @growth.setter
    def growth(self, value):
        self._growth = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def update(self, movement=None) -> None:
        if movement is not None:
            pos_x = self.position[0] + movement[0]
            pox_y = self.position[1] + movement[1]
            self.position = (pos_x, pox_y)
        self.rect.bottomleft = self.position

    def delete(self) -> None:
        self.kill()
