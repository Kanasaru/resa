import pygame
from src.handler import RESA_CH, RESA_EH, RESA_SSH


class Rock(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], image: pygame.image) -> None:
        pygame.sprite.Sprite.__init__(self)

        # image and sprite settings
        self.image = image
        self.size = RESA_SSH.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2)
        self.image = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.sprite_sheet_id = None
        self.sprite_id = None

        # positions
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.position

    def update(self, event: pygame.event.Event = None) -> None:
        if event is not None:
            if event.type == RESA_EH.GAME_EVENT:
                if event.code == RESA_EH.CTRL_MAP_MOVE:
                    pos_x = self.position[0] + event.move[0]
                    pox_y = self.position[1] + event.move[1]
                    self.position = (pos_x, pox_y)
        self.rect.bottomleft = self.position
