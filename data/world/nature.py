import pygame


class Tree(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], size: tuple[int, int], image: pygame.image) -> None:
        pygame.sprite.Sprite.__init__(self)

        self._position = position
        self.image = image
        self.size = size

        rect = self.image.get_rect()
        height = rect.height
        width = rect.width
        ratio = self.size[0] / width
        new_height = int(height * ratio)
        self.size = (self.size[0], new_height)

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

    def update(self) -> None:
        self.rect.bottomleft = self.position

    def move(self, movement: tuple[int, int]) -> None:
        pos_x = self.position[0] + movement[0]
        pox_y = self.position[1] + movement[1]
        self.position = (pos_x, pox_y)

    def delete(self) -> None:
        self.kill()
