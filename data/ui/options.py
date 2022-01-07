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


class Options(forms.Interface):
    def __init__(self, sheet_handler: SpriteSheetHandler):
        super().__init__()

        self.sheet_handler = sheet_handler
        self.sheet_key = conf.sp_menu_btn_key
        self.swt_sheet_key = conf.sp_menu_swt_key

        self.rect = pygame.Rect((0, 0), conf.resolution)
        self.bg_color = forms.COLOR_BLACK
        self.bg_image = conf.background_image
        self.__credits = f"{locales.get('info_credits')} {conf.author} | {conf.www}"

        self.screenmodes = self.get_screenmodes()

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
                    pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_CHG_RESOLUTION, res=mode)
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
                    pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_CHG_RESOLUTION, res=mode)
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
                pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_SWT_FULLSCREEN,
                                   fullscreen=True, res=self.screenmodes['full'][0]),
                pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_SWT_FULLSCREEN,
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
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_BTN_MAINMENU)
        )
        b_back.align(forms.CENTER)

        # add form objects to title
        self.title.add([tf_headline, tf_version, tf_credits, l_reso])
        self.title.add(b_back)

    @staticmethod
    def get_screenmodes() -> dict[str, list]:
        """ Returns a dictionary of 'full' and 'win' screen sizes

        :return: dictionary['full' and 'win'][list of screen sizes]
        """
        screenmodes = {
            'full': list(),
            'win': list(),
        }
        desktop_sizes = pygame.display.get_desktop_sizes()
        desktop_w = desktop_sizes[0][0]
        desktop_h = desktop_sizes[0][1]

        for reso in pygame.display.list_modes():
            if reso[0] < 800 or reso[0] > 1280 or reso[1] < 600:
                pass
            else:
                insert = True
                for value in screenmodes['full']:
                    w, h = value
                    if reso[0] == w:
                        insert = False
                if insert:
                    screenmodes['full'].append(reso)

        if desktop_w > 1280 and desktop_h > 960:
            screenmodes['win'].append((1280, 960))
        if desktop_w > 1000 and desktop_h > 600:
            screenmodes['win'].append((1000, 720))
        if desktop_w > 800 and desktop_h > 600:
            screenmodes['win'].append((800, 600))

        return screenmodes
