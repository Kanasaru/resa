""" This module provides the GamePanel class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
from data.handlers.locals import LocalsHandler
from data.settings import conf
import logging
import pygame
from data.handlers.spritesheet import SpriteSheetHandler
from data.interfaces.interface import Interface
from data.forms.label import Label
from data.forms.title import Title
from data.forms.button import Button
import data.eventcodes as ecodes


class GamePanel(Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler, sheet_key):
        super().__init__()
        self.sheet_handler = sheet_handler
        self.sheet_key = sheet_key

        self.rect = pygame.Rect((0, 0), (conf.resolution[0], 30))
        self.bg_color = conf.COLOR_BLACK
        self.bg_image = None
        self._resources = f"{LocalsHandler.lang('res_wood')}: 0 | " \
                          f"{LocalsHandler.lang('res_stone')}: 0 | " \
                          f"{LocalsHandler.lang('res_marble')}: 0 | " \
                          f"{LocalsHandler.lang('res_tools')}: 0 | " \
                          f"{LocalsHandler.lang('res_gold')}: 0"

        self.title = Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(255)

        # labels
        tf_resources = Label((self.title.width() // 2, 5), self.resources, 14, self.update_resources)
        tf_resources.set_font(conf.std_font)
        tf_resources.font_color(conf.COLOR_WHITE)
        tf_resources.align(tf_resources.CENTER)
        # buttons
        b_quit = Button(
            pygame.Rect(self.title.width() - 5, 3, 70, 24),
            self.sheet_handler,
            self.sheet_key,
            LocalsHandler.lang('btn_leavegame'),
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_LEAVEGAME)
        )
        b_quit.align(b_quit.RIGHT)
        b_quit.set_font(conf.std_font, 13)
        b_save = Button(
            pygame.Rect(self.title.width() - 80, 3, 70, 24),
            self.sheet_handler,
            self.sheet_key,
            LocalsHandler.lang('btn_savegame'),
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_SAVEGAME)
        )
        b_save.align(b_save.RIGHT)
        b_save.set_font(conf.std_font, 13)
        b_save.disable()

        self.title.add(tf_resources)
        self.title.add([b_save, b_quit])

    @property
    def resources(self) -> str:
        return self._resources

    @resources.setter
    def resources(self, res: dict) -> None:
        try:
            self._resources = f"{LocalsHandler.lang('res_wood')}: {res['Wood']} | " \
                              f"{LocalsHandler.lang('res_stone')}: {res['Stone']} | " \
                              f"{LocalsHandler.lang('res_marble')}: {res['Marble']} | " \
                              f"{LocalsHandler.lang('res_tools')}: {res['Tools']} | " \
                              f"{LocalsHandler.lang('res_gold')}: {res['Gold']}"
        except KeyError:
            logging.warning('Failed to set resources in GamePanel')
        finally:
            pass

    def update_resources(self):
        return self.resources
