""" This module provides the MainMenu class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
import data.eventcodes as ecodes
import data.ui.form as forms
from data.handlers.spritesheet import SpriteSheetHandler
import data.locales as locales
from data.settings import conf


class MainMenu(forms.Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler, sheet_key):
        super().__init__()

        self.sheet_handler = sheet_handler
        self.sheet_key = sheet_key

        self.rect = pygame.Rect((0, 0), pygame.display.get_surface().get_size())
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = conf.background_image
        self.__credits = f"{locales.get('info_credits')} {conf.author} | {conf.www}"

        self.build()

    def build(self):
        self.title = forms.Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(255)

        # labels
        tf_headline = forms.Label((int(self.title.width() / 2), 20), conf.title.upper(), 90)
        tf_headline.align(forms.CENTER)
        tf_version = forms.Label((self.title.width() - 5, 5), f'v{conf.version}', 14)
        tf_version.align(forms.RIGHT)
        tf_credits = forms.Label((int(self.title.width() / 2), self.title.height() - 24), self.__credits, 14)
        tf_credits.align(forms.CENTER)
        # buttons
        width, height = tf_headline.get_dimensions()
        position_y = height + 70
        b_newgame = forms.Button(
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            locales.get('btn_newgame'),
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_STARTGAME)
        )
        b_newgame.align(forms.CENTER)
        position_y += b_newgame.height() + 20
        b_loadgame = forms.Button(
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            locales.get('btn_loadgame'),
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_LOADGAME)
        )
        b_loadgame.align(forms.CENTER)
        try:
            f = open(conf.save_file)
            f.close()
        except FileNotFoundError:
            b_loadgame.disable()
        position_y += b_loadgame.height() + 20
        b_options = forms.Button(
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            locales.get('btn_options'),
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_OPTIONS)
        )
        b_options.align(forms.CENTER)
        position_y += b_options.height() + 20
        b_quitgame = forms.Button(
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            locales.get('btn_quitgame'),
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_QUITGAME)
        )
        b_quitgame.align(forms.CENTER)

        b_editor = forms.Button(
            pygame.Rect(10, self.title.height() - 40, 110, 30),
            self.sheet_handler, self.sheet_key,
            locales.get('btn_editor'),
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_EDITOR)
        )
        b_editor.align(forms.LEFT)

        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits])
        self.title.add([b_newgame, b_loadgame, b_options, b_quitgame, b_editor])
