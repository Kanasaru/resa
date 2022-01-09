""" This module provides titles

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
import src.ui.display
import src.ui.form as forms
from src.handler.spritesheet import SpriteSheetHandler
import src.locales as locales
from src.handler import conf
import src.handler


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
            pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_BTN_STARTGAME)
        )
        b_newgame.align(forms.CENTER)
        position_y += b_newgame.height() + 20
        b_loadgame = forms.Button(
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            locales.get('btn_loadgame'),
            pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_BTN_LOADGAME)
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
            pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_BTN_OPTIONS)
        )
        b_options.align(forms.CENTER)
        position_y += b_options.height() + 20
        b_quitgame = forms.Button(
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            locales.get('btn_quitgame'),
            pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_BTN_QUITGAME)
        )
        b_quitgame.align(forms.CENTER)

        b_editor = forms.Button(
            pygame.Rect(10, self.title.height() - 40, 110, 30),
            self.sheet_handler, self.sheet_key,
            locales.get('btn_editor'),
            pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_BTN_EDITOR)
        )
        b_editor.align(forms.LEFT)

        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits])
        self.title.add([b_newgame, b_loadgame, b_options, b_quitgame, b_editor])


class Options(forms.Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler, sheet_key):
        super().__init__()

        self.sheet_handler = sheet_handler
        self.sheet_key = sheet_key
        self.swt_sheet_key = conf.sp_menu_swt_key

        self.rect = pygame.Rect((0, 0), pygame.display.get_surface().get_size())
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = conf.background_image
        self.__credits = f"{locales.get('info_credits')} {conf.author} | {conf.www}"

        self.screenmodes = src.ui.display.get_screenmodes()

        if not self.screenmodes['full'] and not self.screenmodes['win']:
            raise RuntimeError('No resolution. No game.')

        self.build()

    def build(self):
        self.title = forms.Title(self.rect, self.bg_color, self.bg_image)
        self.title.set_alpha(255)

        # labels
        tf_headline = forms.Label((self.title.width() // 2, 20), conf.title.upper(), 90)
        tf_headline.align(forms.CENTER)
        tf_version = forms.Label((self.title.width() - 5, 5), f'v{conf.version}', 14)
        tf_version.align(forms.RIGHT)
        tf_credits = forms.Label((self.title.width() // 2, self.title.height() - 24), self.__credits, 14)
        tf_credits.align(forms.CENTER)
        width, height = tf_headline.get_dimensions()
        position_y = height + 20
        l_reso = forms.Label((self.title.width() // 2, position_y), f"{locales.get('info_resolution')}", 40)
        l_reso.align(forms.CENTER)
        # buttons
        position_y += l_reso.height() + 20

        if conf.fullscreen:
            for mode in self.screenmodes['full'][0:3]:
                btn = forms.Button(
                    pygame.Rect(self.title.width() / 2, position_y, 180, 50),
                    self.sheet_handler, self.sheet_key,
                    f'{mode[0]}x{mode[1]}',
                    pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_BTN_CHG_RESOLUTION, res=mode)
                )
                btn.align(forms.CENTER)
                if pygame.display.get_surface().get_size() == mode:
                    btn.disable()
                self.title.add(btn)
                position_y += btn.height() + 20
        else:
            for mode in self.screenmodes['win']:
                btn = forms.Button(
                    pygame.Rect(self.title.width() / 2, position_y, 180, 50),
                    self.sheet_handler, self.sheet_key,
                    f'{mode[0]}x{mode[1]}',
                    pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_BTN_CHG_RESOLUTION, res=mode)
                )
                btn.align(forms.CENTER)
                if pygame.display.get_surface().get_size() == mode:
                    btn.disable()
                self.title.add(btn)
                position_y += btn.height() + 20

        if self.screenmodes['full']:
            l_fullscreen = forms.Label((int(self.title.width() / 2), position_y),
                                       f"{locales.get('l_fullscreen')}:", 20)
            swt_fullscreen = forms.Switch(
                pygame.Rect(self.title.width() / 2, position_y, 60, 30),
                self.sheet_handler, self.swt_sheet_key,
                pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_SWT_FULLSCREEN,
                                   fullscreen=True, res=self.screenmodes['full'][0]),
                pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_SWT_FULLSCREEN,
                                   fullscreen=False, res=self.screenmodes['full'][-1]),
                conf.fullscreen
            )
            swt_fullscreen.pos_x = self.title.width() // 2 + l_fullscreen.width() // 2 + 5
            l_fullscreen.pos_x = self.title.width() // 2 - swt_fullscreen.width() // 2 - 5
            swt_fullscreen.align(forms.CENTER)
            l_fullscreen.align(forms.CENTER)
            self.title.add([swt_fullscreen, l_fullscreen])
            position_y += swt_fullscreen.height() + 20

        b_back = forms.Button(
            pygame.Rect(self.title.width() / 2, position_y, 220, 60),
            self.sheet_handler, self.sheet_key,
            locales.get('btn_back'),
            pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_BTN_MAINMENU)
        )
        b_back.align(forms.CENTER)

        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits, l_reso])
        self.title.add(b_back)
