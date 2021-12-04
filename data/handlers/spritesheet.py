import logging
import pygame


class SpriteSheet(object):
    def __init__(self, key: str, filename: str, sprite_size: tuple[int, int]) -> None:
        self._key = key
        try:
            self._sheet = pygame.image.load(filename).convert()
        except FileNotFoundError as e:
            logging.error(e)
            self._sheet = pygame.Surface((0, 0))
        self._sheet_size = self.sheet.get_size()
        self._sprite_size = sprite_size
        self.pattern = {}
        self._colorkey = None
        self.__generate_pattern()

    @property
    def key(self):
        return self._key

    @property
    def sheet(self):
        return self._sheet

    @property
    def sheet_size(self):
        return self._sheet_size

    @property
    def sprite_size(self):
        return self._sprite_size

    @property
    def colorkey(self):
        return self._colorkey

    @colorkey.setter
    def colorkey(self, value):
        self._colorkey = value

    def __generate_pattern(self):
        sprite_width, sprite_height = self.sprite_size  # 128, 64
        sheet_width, sheet_height = self.sheet_size  # 1024, 384
        sprites_per_col = sheet_width // sprite_width  # 8
        sprites_per_row = sheet_height // sprite_height  # 6
        index = pos_x = pos_y = 0
        for row in range(sprites_per_row):
            for col in range(sprites_per_col):
                self.pattern[index] = (pos_x, pos_y, sprite_width, sprite_height)
                pos_x = (col + 1) * sprite_width
                index += 1
            pos_x = 0
            pos_y = (row + 1) * sprite_height

    def __bool__(self):
        if self.sheet_size == (0, 0):
            return False
        return True


class SpriteSheetHandler(object):
    def __init__(self):
        self._sheets = []

    @property
    def sheets(self):
        return self._sheets

    @sheets.setter
    def sheets(self, sheet):
        self._sheets.append(sheet)

    def add(self, sheet: SpriteSheet):
        for sh in self.sheets:
            if sh.key == sheet.key:
                logging.error('Key of given sprite sheet already exists. Not added.')
        self.sheets = sheet
        if not sheet:
            logging.error('Given sheet is empty. Loaded it anyway.')

    def image_by_index(self, key: str, index: int) -> pygame.Surface:
        # check if key is in list
        sheet = None
        for sh in self.sheets:
            if sh.key == key:
                sheet = sh
        if sheet is None:
            raise KeyError(f'Given key does not exists: {key}')
        # get image
        rect = pygame.Rect(sheet.pattern[index])
        image = pygame.Surface(rect.size).convert()
        image.blit(sheet.sheet, (0, 0), rect)
        image.set_colorkey(sheet.colorkey, pygame.RLEACCEL)

        return image

    @staticmethod
    def aspect_ratio(size: tuple[int, int], width: int = -1, height: int = -1) -> tuple[int, int]:
        if width != -1:
            ratio = width / size[0]
            new_height = int(size[1] * ratio)
            new_width = width
        elif height != -1:
            ratio = height / size[1]
            new_width = int(size[0] * ratio)
            new_height = height
        else:
            logging.warning('No size, no ratio. Returned original size.')
            return size

        return new_width, new_height
