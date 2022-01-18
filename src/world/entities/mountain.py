import pygame
from src.handler import RESA_CH, RESA_EH, RESA_SSH


class Mountain(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], image: pygame.image) -> None:
        pygame.sprite.Sprite.__init__(self)

        # image and sprite settings
        self.image = image
        self.size = RESA_SSH.aspect_ratio(self.image.get_rect().size, RESA_CH.grid_zoom * 2 * 5)
        self.image = pygame.transform.scale(self.image, self.size).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.sprite_sheet_id = None
        self.sprite_id = None
        self.ores = ores = {
            'Gold': False,
            'Iron': False,
            'Gems': False
        }

        # positions
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.position

    def update(self, event: pygame.event.Event = None) -> None:
        if event is not None:
            if event.type == RESA_EH.RESA_GAME_EVENT:
                if event.code == RESA_EH.RESA_CTRL_MAP_MOVE:
                    pos_x = self.position[0] + event.move[0]
                    pox_y = self.position[1] + event.move[1]
                    self.position = (pos_x, pox_y)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pos_in_mask = event.pos[0] - self.rect.x, event.pos[1] - self.rect.y
                    collided = self.rect.collidepoint(event.pos) and self.mask.get_at(pos_in_mask)
                    if collided:
                        print(self.ores)

        self.rect.midbottom = self.position
