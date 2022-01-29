import logging
import pygame
import src.ui.form as forms
from src.handler import RESA_EH, RESA_SSH, RESA_GSH
import src.locales as locales


class GamePanel(forms.Interface):
    def __init__(self, sheet_key):
        super().__init__()
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
            RESA_SSH,
            self.sheet_key,
            locales.get('btn_leavegame'),
            pygame.event.Event(RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_BTN_LEAVEGAME)
        )
        b_quit.align(forms.RIGHT)
        b_quit.set_font(False, 13)
        b_save = forms.Button(
            pygame.Rect(self.title.width() - 80, 3, 70, 24),
            RESA_SSH,
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


BUILD_MENU_FARMS = 0
BUILD_MENU_INFRASTRUCTURE = 1
BUILD_MENU_GENERAL = 2


class BuildMenuIcons(forms.Interface):
    def __init__(self):
        super().__init__()

        # basics
        self.rect = pygame.Rect((0, 0), pygame.display.get_surface().get_size())
        self.bg_color = forms.COLOR_KEY
        self.button_width = 64
        self.button_height = 64
        self.current_menu = -1

        self.build()

    def build(self):
        # basic title setup
        self.title = forms.Title(self.rect, self.bg_color, None, self.bg_color)
        self.title.set_alpha(255)

        # buttons
        x = self.title.width() - 20
        y = 55
        btn_1 = forms.IconButton(
            pygame.Rect(x, y, self.button_width, self.button_height),
            'IconButtons',
            RESA_SSH.image_by_index('Icons', 0),
            pygame.event.Event(RESA_EH.RESA_GAME_EVENT, code=RESA_EH.RESA_BUILD_MENU, menu=BUILD_MENU_GENERAL)
        )
        btn_1.align(forms.RIGHT)
        if self.current_menu == BUILD_MENU_GENERAL:
            btn_1.active = True
        y += btn_1.height() + 10
        btn_2 = forms.IconButton(
            pygame.Rect(x, y, self.button_width, self.button_height),
            'IconButtons',
            RESA_SSH.image_by_index('Icons', 1),
            pygame.event.Event(RESA_EH.RESA_GAME_EVENT, code=RESA_EH.RESA_BUILD_MENU, menu=BUILD_MENU_FARMS)
        )
        btn_2.align(forms.RIGHT)
        if self.current_menu == BUILD_MENU_FARMS:
            btn_2.active = True
        y += btn_2.height() + 10
        btn_3 = forms.IconButton(
            pygame.Rect(x, y, self.button_width, self.button_height),
            'IconButtons',
            RESA_SSH.image_by_index('Icons', 2),
            pygame.event.Event(RESA_EH.RESA_GAME_EVENT, code=RESA_EH.RESA_BUILD_MENU, menu=BUILD_MENU_INFRASTRUCTURE)
        )
        btn_3.align(forms.RIGHT)
        if self.current_menu == BUILD_MENU_INFRASTRUCTURE:
            btn_3.active = True
        y += btn_3.height() + 10
        btn_4 = forms.IconButton(
            pygame.Rect(x, y, self.button_width, self.button_height),
            'IconButtons',
            RESA_SSH.image_by_index('Icons', 0),
            pygame.event.Event(RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_BTN_LEAVEGAME)
        )
        btn_4.align(forms.RIGHT)
        y += btn_4.height() + 10

        self.title.add([btn_1, btn_2, btn_3, btn_4])

        # build menu
        if self.current_menu == BUILD_MENU_GENERAL:
            x = self.title.width() - 158
            y = 55
            btn_1 = forms.IconButton(
                pygame.Rect(x, y, self.button_width, self.button_height),
                'IconButtons',
                RESA_SSH.image_by_index('Countinghouse', 0),
                pygame.event.Event(RESA_EH.RESA_GAME_EVENT, code=RESA_EH.RESA_BUILDMODE)
            )
            self.title.add([btn_1])
        elif self.current_menu == BUILD_MENU_FARMS:
            x = self.title.width() - 158
            y = 55
            btn_1 = forms.IconButton(
                pygame.Rect(x, y, self.button_width, self.button_height),
                'IconButtons',
                RESA_SSH.image_by_index('Farmfields', 3),
                pygame.event.Event(RESA_EH.RESA_GAME_EVENT, code=RESA_EH.RESA_BUILDMODE)
            )
            self.title.add([btn_1])
        elif self.current_menu == BUILD_MENU_INFRASTRUCTURE:
            pass
        else:
            pass

    def run_logic(self):
        if RESA_GSH.build_menu_open:
            if RESA_GSH.build_menu == BUILD_MENU_GENERAL:
                if self.current_menu == BUILD_MENU_GENERAL:
                    pass
                else:
                    self.current_menu = BUILD_MENU_GENERAL
                    self.build()
            elif RESA_GSH.build_menu == BUILD_MENU_FARMS:
                if self.current_menu == BUILD_MENU_FARMS:
                    pass
                else:
                    self.current_menu = BUILD_MENU_FARMS
                    self.build()
            elif RESA_GSH.build_menu == BUILD_MENU_INFRASTRUCTURE:
                if self.current_menu == BUILD_MENU_INFRASTRUCTURE:
                    pass
                else:
                    self.current_menu = BUILD_MENU_INFRASTRUCTURE
                    self.build()
            else:
                print('ERROR')
        elif self.current_menu != -1:
            self.current_menu = -1
            self.build()

        self.title.run_logic()

    def collide(self, point):
        for value in self.title.form_objects:
            if value.rect.collidepoint(point):
                return True

        return False
