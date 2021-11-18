import pygame


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

        self.solid = False

    def update(self) -> None:
        self.rect.topleft = self.pos

    def set_solid(self, value: bool):
        self.solid = value

    def position(self, position: tuple = None) -> tuple | bool:
        if position is not None:
            self.pos = position
            return True
        return self.pos

    def move(self, movement: tuple) -> None:
        pos_x = self.pos[0] + movement[0]
        pox_y = self.pos[1] + movement[1]
        self.pos = (pos_x, pox_y)

    def delete(self) -> None:
        self.kill()
