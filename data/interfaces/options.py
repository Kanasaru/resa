""" This module provides the MainMenu class

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
import pygame
from data.handlers.spritesheet import SpriteSheetHandler
from data.interfaces.interface import Interface
from data.forms.label import Label
from data.forms.title import Title
from data.forms.button import Button
from data.forms.switch import Switch
import data.eventcodes as ecodes


class Options(Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler):
        super().__init__()

        self.sheet_handler = sheet_handler
        self.sheet_key = conf.sp_menu_btn_key
        self.swt_sheet_key = conf.sp_menu_swt_key

        self.rect = pygame.Rect((0, 0), conf.resolution)
        self.bg_color = conf.COLOR_BLACK
        self.bg_image = conf.background_image
        self.__credits = f'Created and Designed by {conf.author} | {conf.www}'

        self.build()

    def build(self):
        self.title = Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(255)

        # labels
        tf_headline = Label((int(self.title.width() / 2), 20), conf.title.upper())
        tf_headline.set_font(conf.std_font, 90)
        tf_headline.align(tf_headline.CENTER)
        tf_version = Label((self.title.width() - 5, 5), f'v{conf.version}')
        tf_version.set_font(conf.std_font, 14)
        tf_version.align(tf_version.RIGHT)
        tf_credits = Label((int(self.title.width() / 2), self.title.height() - 24), self.__credits)
        tf_credits.set_font(conf.std_font, 14)
        tf_credits.align(tf_credits.CENTER)
        width, height = tf_headline.get_dimensions()
        position_y = height + 20
        tf_resolution = Label((int(self.title.width() / 2), position_y), 'Resolution')
        tf_resolution.set_font(conf.std_font, 40)
        tf_resolution.align(tf_resolution.CENTER)
        # buttons
        position_y += tf_resolution.height() + 20

        # todo: use a dropdown form for every resolution higher than 800x600
        #       and if not possible calculate by display size 3 possible values
        full_screen_resolutions = pygame.display.list_modes()
        no_fullscreen = True

        if (1920, 1080) in full_screen_resolutions:
            no_fullscreen = False
            b_1920x1080 = Button(
                pygame.Rect(self.title.width() / 2, position_y, 180, 50),
                self.sheet_handler, self.sheet_key,
                '1920x1080',
                pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_CHG_RESOLUTION, res=(1920, 1080))
            )
            b_1920x1080.set_font(conf.std_font)
            b_1920x1080.align(b_1920x1080.CENTER)
            if conf.resolution == (1920, 1080):
                b_1920x1080.disable()
            self.title.add(b_1920x1080)
            position_y += b_1920x1080.height() + 20

        if (1280, 960) in full_screen_resolutions:
            no_fullscreen = False
            b_1280x960 = Button(
                pygame.Rect(self.title.width() / 2, position_y, 180, 50),
                self.sheet_handler, self.sheet_key,
                '1280x920',
                pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_CHG_RESOLUTION, res=(1280, 960))
            )
            b_1280x960.set_font(conf.std_font)
            b_1280x960.align(b_1280x960.CENTER)
            if conf.resolution == (1280, 960):
                b_1280x960.disable()
            self.title.add(b_1280x960)
            position_y += b_1280x960.height() + 20

        if (1280, 800) in full_screen_resolutions:
            no_fullscreen = False
            b_1280x800 = Button(
                pygame.Rect(self.title.width() / 2, position_y, 180, 50),
                self.sheet_handler, self.sheet_key,
                '1280x920',
                pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_CHG_RESOLUTION, res=(1280, 800))
            )
            b_1280x800.set_font(conf.std_font)
            b_1280x800.align(b_1280x800.CENTER)
            if conf.resolution == (1280, 800):
                b_1280x800.disable()
            self.title.add(b_1280x800)
            position_y += b_1280x800.height() + 20

        if (800, 600) in full_screen_resolutions:
            no_fullscreen = False
            b_800x600 = Button(
                pygame.Rect(self.title.width() / 2, position_y, 180, 50),
                self.sheet_handler, self.sheet_key,
                '800x600',
                pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_CHG_RESOLUTION, res=(800, 600))
            )
            b_800x600.set_font(conf.std_font)
            b_800x600.align(b_800x600.CENTER)
            if conf.resolution == (800, 600):
                b_800x600.disable()
            self.title.add(b_800x600)
            position_y += b_800x600.height() + 20

        if no_fullscreen:
            b_800x600 = Button(
                pygame.Rect(self.title.width() / 2, position_y, 180, 50),
                self.sheet_handler, self.sheet_key,
                '800x600',
                pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_CHG_RESOLUTION, res=(800, 600))
            )
            b_800x600.set_font(conf.std_font)
            b_800x600.align(b_800x600.CENTER)
            if conf.resolution == (800, 600):
                b_800x600.disable()
            self.title.add(b_800x600)
            position_y += b_800x600.height() + 20
        else:
            l_fullscreen = Label((int(self.title.width() / 2), position_y), 'Fullscreen:')
            l_fullscreen.set_font(conf.std_font, 20)
            swt_fullscreen = Switch(
                pygame.Rect(self.title.width() / 2, position_y, 60, 30),
                self.sheet_handler, self.swt_sheet_key,
                pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_SWT_FULLSCREEN, fullscreen=True),
                pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_SWT_FULLSCREEN, fullscreen=False),
                conf.fullscreen
            )
            swt_fullscreen.pos_x = int(self.title.width() / 2) + int(l_fullscreen.width() / 2) + 5
            l_fullscreen.pos_x = int(self.title.width() / 2) - int(swt_fullscreen.width() / 2) - 5
            swt_fullscreen.align(swt_fullscreen.CENTER)
            l_fullscreen.align(l_fullscreen.CENTER)
            self.title.add([swt_fullscreen, l_fullscreen])
            position_y += swt_fullscreen.height() + 20

        b_back = Button(
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            'Back',
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_MAINMENU)
        )
        b_back.set_font(conf.std_font)
        b_back.align(b_back.CENTER)

        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits, tf_resolution])
        self.title.add(b_back)
