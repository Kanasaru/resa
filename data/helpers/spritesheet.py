import pygame


class SpriteSheet(object):
    def __init__(self, filename, sprite_size):
        try:
            self.sheet = pygame.image.load(filename).convert()
            self.sheet_size = self.sheet.get_size()
            self.sprite_size = sprite_size
        except:
            print("Can't find file")

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    def image_rotate(self, image, angle):
        image_new = pygame.transform.rotate(image, angle)
        return image_new

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]
