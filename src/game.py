""" This module provides the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import sys
import pygame
import src.locales as locales
from src.handler import RESA_CH, RESA_GSH, RESA_MH, RESA_EH, RESA_DH, RESA_GDH, RESA_SSH
from src.ui.form import MessageHandler
import src.ui.display
import src.ui.titles as titles
import src.ui.screens as screens
import src.ui.panels as panels
from src.ui.editor import Editor
from src.world.map import Map
from src.world.entities import farmfields
from src.world.entities.building import Building


class Game(object):
    def __init__(self):
        # display and surface
        self.surface = pygame.display.get_surface()
        pygame.display.set_icon(pygame.image.load(RESA_CH.icon).convert())
        pygame.display.set_caption(f"{locales.get('info_welcome')} {RESA_CH.title}")

        # init messages
        self.messages = MessageHandler('MenuButtons')

        # init menu
        RESA_GSH.current_menu = titles.MAINMENU

        # init map
        self.map = Map(self.surface.get_size())

        # timer
        pygame.time.set_timer(RESA_EH.AUTOSAVE_EVENT, RESA_CH.autosave_interval)
        pygame.time.set_timer(RESA_EH.GAME_CLOCK, RESA_CH.game_speed)

    def run(self) -> None:
        # start music handler
        RESA_MH.start(RESA_CH.volume)
        # start game loop
        while not RESA_GSH.exit_resa:
            RESA_GSH.clock.tick(RESA_CH.fps)
            self.handle_events()
            self.run_logic()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            # timer and auto events
            elif event.type == RESA_EH.AUTOSAVE_EVENT and RESA_CH.autosave:
                pass
            elif event.type == RESA_EH.MUSIC_ENDED_EVENT:
                if len(RESA_MH.playlist) > 0:
                    RESA_MH.load_next()
                else:
                    RESA_MH.refill()
            elif event.type == RESA_EH.GAME_CLOCK:
                pass
            # title events
            elif event.type == RESA_EH.TITLE_EVENT:
                if event.code == RESA_EH.QUITGAME_TRUE:
                    if RESA_GSH.game_running:
                        RESA_GSH.game_running = False
                    else:
                        RESA_GSH.exit_resa = True
                        self.exit()
                elif event.code == RESA_EH.QUITGAME_FALSE:
                    RESA_GDH.pause_ingame_time()
                elif event.code == RESA_EH.BTN_STARTGAME:
                    RESA_GSH.game_running = True
                    self.map.build_world()
                    RESA_GDH.start_timer()
                elif event.code == RESA_EH.BTN_LOADGAME:
                    pass
                elif event.code == RESA_EH.BTN_OPTIONS:
                    RESA_GSH.current_menu = titles.OPTIONSMENU
                elif event.code == RESA_EH.BTN_QUITGAME:
                    self.exit()
                elif event.code == RESA_EH.BTN_MAINMENU:
                    RESA_GSH.current_menu = titles.MAINMENU
                elif event.code == RESA_EH.BTN_EDITOR:
                    self.editor()
                elif event.code == RESA_EH.BTN_LEAVEGAME:
                    RESA_GDH.pause_ingame_time()
                    self.exit()
            # keyboard events
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F1:
                    pass
                elif event.key == pygame.K_F2:
                    self.messages.info(src.ui.display.take_screenshot())
                elif event.key == pygame.K_F3:
                    RESA_DH.toggle()
                elif event.key == pygame.K_p:
                    if RESA_GSH.game_running:
                        RESA_GSH.pause_game = not RESA_GSH.pause_game
                        RESA_GDH.pause_ingame_time()
                    RESA_MH.pause()
                elif event.key == pygame.K_PLUS:
                    RESA_MH.volume += .1
                elif event.key == pygame.K_MINUS:
                    RESA_MH.volume -= .1
            # mouse events
            elif event.type == pygame.MOUSEBUTTONUP:
                if RESA_GSH.game_running:
                    if event.button == 1:
                        # cursor in map?
                        cursor_map = self.map.cursor_on_map(event.pos)
                        if cursor_map and not self.messages.is_msg():
                            # build mode
                            if RESA_GSH.building and not RESA_GSH.cursor_over_icons:
                                RESA_GSH.place = True
                                RESA_GSH.place_on = self.map.world.grid.pos_in_iso_grid_field(cursor_map)
                    elif event.button == 2:
                        pass
            elif event.type == pygame.MOUSEMOTION:
                if self.map.cursor_on_map(event.pos) and not self.messages.is_msg():
                    # cursor not on icons?
                    if panels.ICONS.collide(event.pos):
                        RESA_GSH.cursor_over_icons = True
                    else:
                        RESA_GSH.cursor_over_icons = False
            # game events
            elif event.type == RESA_EH.GAME_EVENT:
                if event.code == RESA_EH.BUILDMODE:
                    RESA_GSH.build_menu_open = False
                    RESA_GSH.build_menu = -1
                    RESA_GSH.building = not RESA_GSH.building
                elif event.code == RESA_EH.BUILD_MENU:
                    if RESA_GSH.build_menu_open:
                        if event.menu == RESA_GSH.build_menu:
                            RESA_GSH.build_menu_open = False
                        else:
                            RESA_GSH.building = False
                            RESA_GSH.build_menu = event.menu
                    else:
                        RESA_GSH.building = False
                        RESA_GSH.build_menu_open = True
                        RESA_GSH.build_menu = event.menu

            # pass-through event
            self.messages.handle_event(event)
            if not self.messages.is_msg():
                if RESA_GSH.game_running:
                    self.map.handle_event(event)
                    panels.ICONS.handle_event(event)
                else:
                    RESA_GSH.current_menu.handle_event(event)

            if RESA_DH:
                screens.DEBUG.handle_event(event)

    def run_logic(self):
        self.messages.run_logic()
        if not self.messages.is_msg():
            if RESA_GSH.game_running:
                # update in-game time
                if RESA_DH:
                    screens.DEBUG.timer = RESA_DH.play_time
                RESA_GDH.update()
                self.map.run_logic()
                panels.ICONS.run_logic()

                if not RESA_GSH.pause_game:
                    # check for build mode
                    if RESA_GSH.building and RESA_GSH.place:
                        if self.place_building():
                            print('build')
                        else:
                            print('build not possible')
            else:
                RESA_GSH.current_menu.run_logic()

        if RESA_DH:
            RESA_DH.update()
            screens.DEBUG.run_logic()

    def render(self):
        # fill surface
        self.surface.fill(RESA_CH.COLOR_WHITE)

        if RESA_GSH.game_running:
            self.map.render(self.surface)
            panels.ICONS.render(self.surface)
            # render pause screen
            if RESA_GSH.pause_game:
                screens.PAUSE.render(self.surface)
        else:
            RESA_GSH.current_menu.render(self.surface)

        if RESA_DH:
            screens.DEBUG.render(self.surface)

        # render messages
        self.messages.render(self.surface)

        # display surface
        pygame.display.flip()

    def exit(self):
        if RESA_GSH.exit_resa:
            print(locales.get('resa_exit'))
            pygame.quit()
            sys.exit()
        # display exit dialog
        self.messages.show(locales.get('msg_cap_leavegame'), locales.get('msg_text_leavegame'),
                           pygame.event.Event(RESA_EH.TITLE_EVENT, code=RESA_EH.QUITGAME_TRUE),
                           locales.get('btn_msg_yes'),
                           pygame.event.Event(RESA_EH.TITLE_EVENT, code=RESA_EH.QUITGAME_FALSE),
                           locales.get('btn_msg_no'))

    @staticmethod
    def editor():
        pygame.display.set_caption(f"{locales.get('info_editor_title')} {RESA_CH.title}")
        pygame.display.set_mode((1280, 960))
        editor = Editor()
        editor.run()
        pygame.display.set_caption(f"{locales.get('info_welcome')} {RESA_CH.title}")
        pygame.display.set_mode((1000, 800))

    def place_building(self):
        # check if placable
        neighbors = self.map.world.grid.iso_grid_neighbors(RESA_GSH.place_on.key)
        build = False
        x, y = RESA_GSH.building_size
        # 1x1
        if x == y == 1:
            raw_field = self.map.world.grid_fields[RESA_GSH.place_on.key]
            if raw_field.solid and raw_field.buildable and not raw_field.building:
                build = True
        # 2x2
        elif x == y == 2:
            if neighbors.top and neighbors.topleft and neighbors.topright:
                raw_field = self.map.world.grid_fields[neighbors.top]
                if raw_field.solid and raw_field.buildable and not raw_field.building:
                    raw_field = self.map.world.grid_fields[neighbors.topleft]
                    if raw_field.solid and raw_field.buildable and not raw_field.building:
                        raw_field = self.map.world.grid_fields[neighbors.topright]
                        if raw_field.solid and raw_field.buildable and not raw_field.building:
                            build = True
        # 3x3
        elif x == y == 3:
            build = True
            for rawval in neighbors.all:
                raw_field = self.map.world.grid_fields[rawval]
                if not raw_field.solid or not raw_field.buildable or raw_field.building:
                    build = False

        if build:
            # delete entities and place building
            # 1x1
            if x == y == 1:
                self.map.world.grid_fields[RESA_GSH.place_on.key].sprite = None
                self.map.world.grid_fields[RESA_GSH.place_on.key].building = True
                raw_field = self.map.world.grid_fields[RESA_GSH.place_on.key]
                new_building = farmfields.Wheat(raw_field.rect.bottomleft)
                self.map.world.grid_fields[RESA_GSH.place_on.key].sprite = new_building
            # 2x2
            elif x == y == 2:
                self.map.world.grid_fields[RESA_GSH.place_on.key].sprite = None
                self.map.world.grid_fields[RESA_GSH.place_on.key].building = True
                self.map.world.grid_fields[neighbors.top].sprite = None
                self.map.world.grid_fields[neighbors.top].building = True
                self.map.world.grid_fields[neighbors.topleft].sprite = None
                self.map.world.grid_fields[neighbors.topleft].building = True
                self.map.world.grid_fields[neighbors.topright].sprite = None
                self.map.world.grid_fields[neighbors.topright].building = True

                raw_field = self.map.world.grid_fields[RESA_GSH.place_on.key]
                new_building = Building(raw_field.rect.midbottom, RESA_SSH.image_by_index('Countinghouse', 0), 2)
                self.map.world.grid_fields[RESA_GSH.place_on.key].sprite = new_building
            # 3x3
            elif x == y == 3:
                self.map.world.grid_fields[RESA_GSH.place_on.key].sprite = None
                for rawval in neighbors.all:
                    self.map.world.grid_fields[rawval].sprite = None
                    self.map.world.grid_fields[rawval].building = True

                raw_field = self.map.world.grid_fields[neighbors.bottom]
                new_building = Building(raw_field.rect.midbottom, RESA_SSH.image_by_index('Countinghouse', 0), 3)
                self.map.world.grid_fields[RESA_GSH.place_on.key].sprite = new_building

        # reset state
        RESA_GSH.place = False
        RESA_GSH.place_on = None

        return build
