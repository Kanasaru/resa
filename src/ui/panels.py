import logging
import pygame
import src.ui.form as forms
from src.handler import RESA_EH
from src.handler.spritesheet import SpriteSheetHandler
import src.locales as locales


class GamePanel(forms.Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler, sheet_key):
        super().__init__()
        self.sheet_handler = sheet_handler
        self.sheet_key = sheet_key

        self.rect = pygame.Rect((0, 0), (pygame.display.get_surface().get_width(), 30))
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = None
        self._resources = f"{locales.get('res_wood')}: 0 | " \
                          f"{locales.get('res_stone')}: 0 | " \
                          f"{locales.get('res_marble')}: 0 | " \
                          f"{locales.get('res_tools')}: 0 | " \
                          f"{locales.get('res_gold')}: 0"

        self.title = forms.Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(255)

        # labels
        tf_resources = forms.Label((self.title.width() // 2, 5), self.resources, 14, self.update_resources)
        tf_resources.font_color(forms.COLOR_WHITE)
        tf_resources.align(forms.CENTER)
        # buttons
        b_quit = forms.Button(
            pygame.Rect(self.title.width() - 5, 3, 70, 24),
            self.sheet_handler,
            self.sheet_key,
            locales.get('btn_leavegame'),
            pygame.event.Event(RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_BTN_LEAVEGAME)
        )
        b_quit.align(forms.RIGHT)
        b_quit.set_font(False, 13)
        b_save = forms.Button(
            pygame.Rect(self.title.width() - 80, 3, 70, 24),
            self.sheet_handler,
            self.sheet_key,
            locales.get('btn_savegame'),
            pygame.event.Event(RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_BTN_SAVEGAME)
        )
        b_save.align(forms.RIGHT)
        b_save.set_font(False, 13)
        b_save.disable()

        self.title.add(tf_resources)
        self.title.add([b_save, b_quit])

    @property
    def resources(self) -> str:
        return self._resources

    @resources.setter
    def resources(self, res: dict) -> None:
        try:
            self._resources = f"{locales.get('res_wood')}: {res['Wood']} | " \
                              f"{locales.get('res_stone')}: {res['Stone']} | " \
                              f"{locales.get('res_marble')}: {res['Marble']} | " \
                              f"{locales.get('res_tools')}: {res['Tools']} | " \
                              f"{locales.get('res_gold')}: {res['Gold']}"
        except KeyError:
            logging.warning('Failed to set resources in GamePanel')
        finally:
            pass

    def update_resources(self):
        return self.resources
