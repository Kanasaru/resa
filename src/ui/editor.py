""" This module provides an editor for islands

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import logging
import pickle
import pygame
from src.handler import RESA_CH, RESA_SSH, RESA_SH, RESA_EH
from datetime import datetime
import src.ui.form as forms
import src.locales as locales
import src.world.grid
from src.world.objects.field import Field, RawField


class PaletteField(pygame.sprite.Sprite):
    def __init__(self, tile, size, position: tuple[int, int], image: pygame.image) -> None:
        """ Holds the src of a single palette field.

        :param tile: identifier of the sprite in its sprite sheet
        :param size: size
        :param position: position of the field
        :param image: sprite image
        """
        pygame.sprite.Sprite.__init__(self)

        # basic settings
        self.size = (size, size)
        self.tile = tile

        # image and sprite settings
        self.image = pygame.transform.scale(image, self.size).convert_alpha()

        # positions
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def update(self, event: pygame.event.Event = None) -> None:
        """ Handles click events and raises new event with the fields tile.

        :param event: event
        :return:
        """
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                pygame.event.post(pygame.event.Event(
                    RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_EDITOR_SELECT, field=self.tile
                ))
        self.rect.topleft = self.position


class Editor(object):
    def __init__(self):
        """ Initializes the editor """
        # event handling varibales
        self.exit = False
        self.selected_tile = False
        self.place_tile = False

        # src
        self.palette_sprites = pygame.sprite.Group()
        self.fields = pygame.sprite.Group()
        self.palette = {
            0: (17, 18), 1: (74, 18), 2: (131, 18), 3: (188, 18), 4: (245, 18), 5: (302, 18),
            6: (17, 75), 7: (74, 75), 8: (131, 75), 9: (188, 75), 10: (245, 75), 11: (302, 75),
            12: (17, 132), 13: (74, 132), 14: (131, 132), 15: (188, 132), 16: (245, 132), 17: (302, 132),
            18: (17, 189), 19: (74, 189), 20: (131, 189), 21: (188, 189), 22: (245, 189), 23: (302, 189),
            24: (17, 246), 25: (74, 246), 26: (131, 246), 27: (188, 246), 28: (245, 246), 29: (302, 246),
            30: (17, 303), 31: (74, 303), 32: (131, 303), 33: (188, 303), 34: (245, 303), 35: (302, 303),
            36: (17, 360), 37: (74, 360), 38: (131, 360), 39: (188, 360), 40: (245, 360), 41: (302, 360),
            42: (17, 417), 43: (74, 417), 44: (131, 417), 45: (188, 417), 46: (245, 417), 47: (302, 417),
            48: (17, 474), 49: (74, 474), 50: (131, 474), 51: (188, 474), 52: (245, 474), 53: (302, 474),
            54: (17, 531), 55: (74, 531), 56: (131, 531), 57: (188, 531), 58: (245, 531), 59: (302, 531),
            60: (17, 588), 61: (74, 588), 62: (131, 588), 63: (188, 588), 64: (245, 588), 65: (302, 588),
            66: (17, 645), 67: (74, 645), 68: (131, 645), 69: (188, 645), 70: (245, 645), 71: (302, 645),
        }

        # set timers and clocks
        self.clock = pygame.time.Clock()

        # set handler
        self.messages = forms.MessageHandler(RESA_SSH, RESA_CH.sp_menu_btn_key)

        # screen settings and build screen
        self.surface = pygame.display.get_surface()
        self.title = self.build_title()

        # load palette
        for key, value in self.palette.items():
            image = RESA_SSH.image_by_index('Tiles', key)
            field = PaletteField(key, 44, (int(value[0]), int(value[1])), image)
            self.palette_sprites.add(field)

        # build grid
        self.shift_x = self.title.width() - 905
        self.shift_y = 25
        RESA_CH.grid = src.world.grid.Grid(44, 44, 20)

        # fill grid with water tiles
        for key, value in RESA_CH.grid.fields_iso.items():
            image = RESA_SSH.image_by_index('Tiles', 2)
            new_field = Field((self.shift_x + value.rect.x, self.shift_y + value.rect.y), image)
            new_field.sprite_sheet_id = 'Tiles'
            new_field.sprite_id = 2
            new_field.iso_key = key
            self.fields.add(new_field)

        # start the game loop
        self.loop()

    def loop(self) -> None:
        """ editor loopp

        :return: None
        """
        while not self.exit:
            self.clock.tick(RESA_CH.fps)
            self.handle_events()
            self.run_logic()
            self.render()

    def handle_events(self) -> None:
        """ Handles all editor events

        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave_editor()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.take_screenshot()
                elif event.key == pygame.K_ESCAPE:
                    self.selected_tile = False
                    self.messages.info(f"{locales.get('editor_no_tile')}")
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.shift_x <= event.pos[0] <= self.shift_x + RESA_CH.grid.grid_width and \
                            self.shift_y <= event.pos[1] <= self.shift_y + RESA_CH.grid.grid_height:
                        tile_field = RESA_CH.grid.pos_in_iso_grid_field(
                            (abs(event.pos[0] - self.shift_x), abs(event.pos[1] - self.shift_y))
                        )
                        if tile_field and not self.messages.is_msg():
                            pygame.event.post(pygame.event.Event(
                                RESA_EH.RESA_TITLE_EVENT,
                                code=RESA_EH.RESA_EDITOR_PLACE,
                                field=tile_field
                            ))
            elif event.type == RESA_EH.RESA_TITLE_EVENT:
                if event.code == RESA_EH.RESA_EDITOR_SELECT:
                    RESA_SH.play('btn-click')
                    self.selected_tile = event.field
                    self.messages.info(f"{locales.get('editor_tile_select')} {self.selected_tile}.")
                elif event.code == RESA_EH.RESA_EDITOR_PLACE:
                    self.place_tile = event.field
                elif event.code == RESA_EH.RESA_EDITOR_LEAVE:
                    self.leave_editor()
                elif event.code == RESA_EH.RESA_EDITOR_LOAD:
                    self.load_island()
                elif event.code == RESA_EH.RESA_EDITOR_SAVE:
                    self.save_island()
                elif event.code == RESA_EH.RESA_QUITGAME_TRUE:
                    self.exit = True

            self.messages.handle_event(event)
            self.title.handle_event(event)
            self.palette_sprites.update(event)

    def run_logic(self) -> None:
        """ Runs the editor logic

        :return: None
        """
        if self.place_tile:
            if self.selected_tile:
                for field in self.fields:
                    if field.iso_key == self.place_tile.key:
                        field.image = pygame.transform.scale(
                            RESA_SSH.image_by_index('Tiles', self.selected_tile),
                            field.size).convert_alpha()
                        field.sprite_id = self.selected_tile

            self.place_tile = False

        self.messages.run_logic()
        self.title.run_logic()

    def render(self) -> None:
        """ Renders everything to the surface

        :return: None
        """
        self.surface.fill(RESA_CH.COLOR_WHITE)

        self.title.render(self.surface)

        self.palette_sprites.draw(self.surface)

        self.fields.draw(self.surface)

        RESA_CH.grid.draw_iso_grid(self.surface, (self.shift_x, self.shift_y))

        # render message and info boxes
        self.messages.render(self.surface)

        pygame.display.flip()

    def take_screenshot(self) -> None:
        """ Saves the current screen as an image.

        :return: None
        """
        RESA_SH.play('screenshot')
        filename = f'{RESA_CH.screenshot_path}screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        pygame.image.save(pygame.display.get_surface(), filename)
        self.messages.info(f"{locales.get('info_screenshot')}: {filename}")
        logging.info('Took screenshot')

    def leave_editor(self) -> None:
        """ Shows leaving message dialog box.

        :return: None
        """
        self.messages.show(locales.get('msg_cap_leaveeditor'), locales.get('msg_text_leaveeditor'),
                           pygame.event.Event(RESA_EH.RESA_TITLE_EVENT,
                                              code=RESA_EH.RESA_QUITGAME_TRUE),
                           locales.get('btn_msg_yes'),
                           pygame.event.Event(RESA_EH.RESA_TITLE_EVENT,
                                              code=RESA_EH.RESA_QUITGAME_FALSE),
                           locales.get('btn_msg_no'))

    def save_island(self) -> None:
        """ Saves created island in a src file.

        :return: None
        """
        raw_fields = []
        for field in self.fields:
            raw_field = RawField()
            raw_field.pos = field.position
            raw_field.sprite_index = field.sprite_id
            raw_field.sprite_sheet = field.sprite_sheet_id
            raw_field.solid = field.solid
            raw_field.iso_key = field.iso_key
            raw_fields.append(raw_field)

        pickle.dump(raw_fields, open('data/saves/data.island', 'wb'))

    def load_island(self) -> None:
        """ Loads island from its src file.

        :return: None
        """
        self.fields.empty()
        for field_data in pickle.load(open('data/saves/data.island', 'rb')):
            image = RESA_SSH.image_by_index(field_data.sprite_sheet, field_data.sprite_index)
            field = Field(field_data.pos, image)
            field.sprite_sheet_id = field_data.sprite_sheet
            field.sprite_id = field_data.sprite_index
            field.solid = field_data.solid
            field.iso_key = field_data.iso_key
            self.fields.add(field)

    def build_title(self):
        title = forms.Title(pygame.Rect((0, 0), (1280, 960)), RESA_CH.COLOR_WHITE, 'res/images/bg_editor.png')
        title.set_alpha(255)

        position_x = 182
        position_y = 715
        b_save_island = forms.Button(
            pygame.Rect(position_x, position_y, 220, 60),
            RESA_SSH, RESA_CH.sp_menu_btn_key,
            locales.get('editor_btn_save'),
            pygame.event.Event(RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_EDITOR_SAVE)
        )
        b_save_island.align(forms.CENTER)

        position_y += 70

        b_load_island = forms.Button(
            pygame.Rect(position_x, position_y, 220, 60),
            RESA_SSH, RESA_CH.sp_menu_btn_key,
            locales.get('editor_btn_load'),
            pygame.event.Event(RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_EDITOR_LOAD)
        )
        b_load_island.align(forms.CENTER)
        try:
            f = open('data/saves/data.island')
            f.close()
        except FileNotFoundError:
            b_load_island.disable()

        position_y += 70

        b_quiteditor = forms.Button(
            pygame.Rect(position_x, position_y, 220, 60),
            RESA_SSH, RESA_CH.sp_menu_btn_key,
            locales.get('editor_btn_leave'),
            pygame.event.Event(RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_EDITOR_LEAVE)
        )
        b_quiteditor.align(forms.CENTER)

        title.add([b_save_island, b_load_island, b_quiteditor])

        return title
