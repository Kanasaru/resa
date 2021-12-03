import logging


class SpriteSheetHandler(object):
    def __init__(self):
        pass

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
