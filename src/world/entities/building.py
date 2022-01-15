import pygame
from src.handler import RESA_CH, RESA_EH
from src.handler.spritesheet import SpriteSheetHandler


class Building(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], image: pygame.image, size: int) -> None:
        """ Initializes a field

        :param position: position on world surface
        :param image: tree image
        """
        pygame.sprite.Sprite.__init__(self)

        # image and sprite settings
        self.image = image
        self.size = SpriteSheetHandler.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2 * size)
        self.image = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.sprite_sheet_id = None
        self.sprite_id = None

        # positions
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.position

    def update(self, event: pygame.event.Event = None) -> None:
        """ Updates tree by its position

        :param event: optional event
        :return: None
        """
        if event is not None:
            if event.type == RESA_EH.RESA_GAME_EVENT:
                if event.code == RESA_EH.RESA_CTRL_MAP_MOVE:
                    pos_x = self.position[0] + event.move[0]
                    pox_y = self.position[1] + event.move[1]
                    self.position = (pos_x, pox_y)
        self.rect.midbottom = self.position
