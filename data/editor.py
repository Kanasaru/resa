import logging
import pickle

import pygame
from datetime import datetime
from data.handlers.locals import LocalsHandler
from data.handlers.sound import SoundHandler
from data.settings import conf
from data.handlers.msg import Message
from data.handlers.spritesheet import SpriteSheet, SpriteSheetHandler
import data.world.grid
from data.forms.title import Title
import data.eventcodes as ecodes
from data.world.objects.field import Field
from data.forms.button import Button
import xml.etree.ElementTree as ETree


class PaletteField(pygame.sprite.Sprite):
    def __init__(self, tile, size, position: tuple[int, int], image: pygame.image) -> None:
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
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                pygame.event.post(pygame.event.Event(
                    ecodes.RESA_TITLE_EVENT, code = ecodes.RESA_EDITOR_SELECT, field=self.tile
                ))
        self.rect.topleft = self.position


class Editor(object):
    def __init__(self):
        pygame.display.set_caption(f'{conf.title} Island Creator')
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.get_surface()
        self.exit = False
        self.sounds = SoundHandler()
        self.sprite_sheet_handler = SpriteSheetHandler()
        buttons = SpriteSheet(conf.sp_menu_btn_key, conf.sp_menu_btn, conf.sp_menu_btn_size)
        buttons.colorkey = (1, 0, 0)
        self.sprite_sheet_handler.add(buttons)
        for key, value in conf.sp_world.items():
            sheet = SpriteSheet(key, value[0], value[1])
            sheet.colorkey = None
            self.sprite_sheet_handler.add(sheet)
        self.messages = Message(self.sprite_sheet_handler, conf.sp_menu_btn_key)

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
        self.palette_sprites = pygame.sprite.Group()
        self.fields = pygame.sprite.Group()

        for key, value in self.palette.items():
            image = self.sprite_sheet_handler.image_by_index('Tiles', key)
            field = PaletteField(key, 44, (int(value[0]), int(value[1])), image)
            self.palette_sprites.add(field)

        self.selected_tile = False
        self.place_tile = False

        self.title = Title(pygame.Rect((0, 0), conf.resolution), conf.COLOR_WHITE, 'resources/images/bg_editor.png')
        self.title.set_alpha(255)

        position_x = 182
        position_y = 715
        b_save_island = Button(
            pygame.Rect(position_x, position_y, 220, 60),
            self.sprite_sheet_handler, conf.sp_menu_btn_key,
            "Save",
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_EDITOR_SAVE)
        )
        b_save_island.set_font(conf.std_font)
        b_save_island.align(b_save_island.CENTER)

        position_y += 70

        b_load_island = Button(
            pygame.Rect(position_x, position_y, 220, 60),
            self.sprite_sheet_handler, conf.sp_menu_btn_key,
            "Load",
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_EDITOR_LOAD)
        )
        b_load_island.set_font(conf.std_font)
        b_load_island.align(b_load_island.CENTER)
        try:
            f = open('saves/island.data')
            f.close()
        except FileNotFoundError:
            b_load_island.disable()

        position_y += 70

        b_quiteditor = Button(
            pygame.Rect(position_x, position_y, 220, 60),
            self.sprite_sheet_handler, conf.sp_menu_btn_key,
            "Leave",
            pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_EDITOR_LEAVE)
        )
        b_quiteditor.set_font(conf.std_font)
        b_quiteditor.align(b_quiteditor.CENTER)

        self.title.add([b_save_island, b_load_island, b_quiteditor])

        self.shift_x = self.title.width() - 905
        self.shift_y = 25
        self.grid_size = 20
        self.grid_fields = 44
        conf.grid = data.world.grid.Grid(self.grid_fields, self.grid_fields, self.grid_size)
        self.grid_pos = (self.shift_x, self.shift_y)

        for key, value in conf.grid.fields_iso.items():
            image = self.sprite_sheet_handler.image_by_index('Tiles', 2)
            new_field = Field((self.shift_x + value.rect.x, self.shift_y + value.rect.y), image)
            new_field.sprite_sheet_id = 'Tiles'
            new_field.sprite_id = 2
            new_field.iso_key = key
            # add to sprite group and go on
            self.fields.add(new_field)

        self.loop()

    def loop(self):
        while not self.exit:
            self.clock.tick(conf.fps)
            self.handle_events()
            self.run_logic()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave_editor()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.take_screenshot()
                elif event.key == pygame.K_ESCAPE:
                    self.selected_tile = False
                    print('No selected')
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.grid_pos[0] <= event.pos[0] <= self.grid_pos[0] + conf.grid.grid_width:
                        if self.grid_pos[1] <= event.pos[1] <= self.grid_pos[1] + conf.grid.grid_height:
                            tile_field = conf.grid.pos_in_iso_grid_field(
                                (abs(event.pos[0] - self.shift_x), abs(event.pos[1] - self.shift_y))
                            )
                            if tile_field:
                                pygame.event.post(pygame.event.Event(
                                    ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_EDITOR_PLACE, field=tile_field
                                ))
            elif event.type == ecodes.RESA_TITLE_EVENT:
                if event.code == ecodes.RESA_EDITOR_SELECT:
                    self.selected_tile = event.field
                    print(f'selected: {self.selected_tile}')
                elif event.code == ecodes.RESA_EDITOR_PLACE:
                    self.place_tile = event.field
                elif event.code == ecodes.RESA_EDITOR_LEAVE:
                    self.leave_editor()
                elif event.code == ecodes.RESA_EDITOR_LOAD:
                    self.load_island()
                elif event.code == ecodes.RESA_EDITOR_SAVE:
                    self.save_island()
                elif event.code == ecodes.RESA_QUITGAME_TRUE:
                    self.exit = True

            self.messages.handle_event(event)
            self.title.handle_event(event)
            self.palette_sprites.update(event)

    def run_logic(self):
        if self.place_tile:
            if self.selected_tile:
                print(f'Plaziere {self.selected_tile} auf {self.place_tile.key}')

                for field in self.fields:
                    if field.iso_key == self.place_tile.key:
                        field.image = pygame.transform.scale(
                            self.sprite_sheet_handler.image_by_index('Tiles', self.selected_tile),
                            field.size).convert_alpha()
                        field.sprite_id = self.selected_tile

            self.place_tile = False

        self.messages.run_logic()
        self.title.run_logic()

    def render(self):
        self.surface.fill(conf.COLOR_WHITE)

        self.title.render(self.surface)

        self.palette_sprites.draw(self.surface)

        self.fields.draw(self.surface)

        conf.grid.draw_iso_grid(self.surface, self.grid_pos)

        # render message and info boxes
        self.messages.render(self.surface)

        pygame.display.flip()

    def take_screenshot(self) -> None:
        self.sounds.play('screenshot')
        filename = f'{conf.screenshot_path}screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        pygame.image.save(pygame.display.get_surface(), filename)
        self.messages.info(f"{LocalsHandler.lang('info_screenshot')}: {filename}")
        logging.info('Took screenshot')

    def leave_editor(self) -> None:
        self.messages.show(LocalsHandler.lang('msg_cap_leaveeditor'), LocalsHandler.lang('msg_text_leaveeditor'),
                           pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_QUITGAME_TRUE),
                           LocalsHandler.lang('btn_msg_yes'),
                           pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_QUITGAME_FALSE),
                           LocalsHandler.lang('btn_msg_no'))

    def save_island(self):
        raw_data = {}
        island = list()

        for field in self.fields:
            raw_data[field.iso_key] = (field.sprite_id,
                                       conf.grid.fields_iso[field.iso_key].row,
                                       conf.grid.fields_iso[field.iso_key].col)
        row = 0
        row_list = list()
        for k, v in raw_data.items():
            if v[1] == row:
                row_list.append(v[0])
            else:
                island.append(row_list)
                row_list = list()
                row += 1
                row_list.append(v[0])

        pickle.dump(island, open('saves/island.data', 'wb'))

    def load_island(self):
        print(pickle.load(open('saves/island.data', 'rb')))