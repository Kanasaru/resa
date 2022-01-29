""" This module provides the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import pygame
from datetime import datetime
import src.locales as locales
from src.handler import RESA_CH, RESA_SSH, RESA_GDH, RESA_GSH, RESA_MH, RESA_DH, RESA_EH
import src.ui.display
from src.ui.editor import Editor
from src.ui.titles import MainMenu, Options
from src.ui.screens import DebugScreen, GamePausedScreen
from src.ui.panels import BuildMenuIcons
from src.ui.form import MessageHandler
from src.world.map import Map
from src.world.entities import farmfields
from src.world.entities.building import Building


class Game(object):
    def __init__(self, load: bool = False) -> None:
        """ Initializes the game

        :param load: load game from file if true
        """
        # event handling varibales
        self.editor = None
        self.game = None

        # set timers and clocks
        self.clock = pygame.time.Clock()

        # build window
        self.surface = pygame.display.get_surface()
        pygame.display.set_icon(pygame.image.load(RESA_CH.icon).convert())
        pygame.display.set_caption(f"{locales.get('info_welcome')} {RESA_CH.title}")

        # event handling varibales
        RESA_GSH.exit_game = False
        RESA_GSH.map_load = load
        RESA_GSH.pause_game = False
        RESA_GSH.building = False

        # screen settings, build screens and panels
        self.surface = pygame.display.get_surface()
        self.border_thickness = RESA_CH.map_border_thickness
        self.border_color = RESA_CH.COLOR_WHITE
        # create titles
        self.title_main = MainMenu('MenuButtons')
        self.title_options = Options('MenuButtons')
        # debug screen
        self.debug_screen = DebugScreen()
        self.debug_screen.add(locales.get('info_fps'), RESA_GSH.clock.get_fps)
        self.debug_screen.add(locales.get('info_version'), lambda: RESA_CH.version)
        self.debug_screen.add(locales.get('info_date'), lambda: datetime.now().strftime("%A, %d. %B %Y"))
        self.debug_screen.add(locales.get('info_ingame_time'), RESA_GDH.get_game_time)
        # game panel
        self.game_panel_icons = BuildMenuIcons()
        # messages
        self.messages = MessageHandler('MenuButtons')
        # pause screen
        self.paused_screen = GamePausedScreen(pygame.Rect((0, 0), self.surface.get_size()))

        # loading map
        self.map = Map(self.surface.get_size())

        # timer
        pygame.time.set_timer(RESA_EH.RESA_AUTOSAVE_EVENT, RESA_CH.autosave_interval)
        pygame.time.set_timer(RESA_EH.RESA_GAME_CLOCK, RESA_CH.game_speed)

    def run(self) -> None:
        """ in-game loopp

        :return: None
        """
        RESA_MH.start(RESA_CH.volume)

        while not RESA_GSH.exit_game:
            RESA_GSH.clock.tick(RESA_CH.fps)
            self.handle_events()
            self.run_logic()
            self.render()

        self.exit()

    def handle_events(self) -> None:
        """ Handles all in-game events

        :return: None
        """
        for event in pygame.event.get():
            # window events
            if event.type == pygame.QUIT:
                self.leave_game()
            # timer and auto events
            elif event.type == RESA_EH.RESA_AUTOSAVE_EVENT and RESA_CH.autosave:
                pass
            elif event.type == RESA_EH.RESA_MUSIC_ENDED_EVENT:
                if len(RESA_MH.playlist) > 0:
                    RESA_MH.load_next()
                else:
                    RESA_MH.refill()
            elif event.type == RESA_EH.RESA_GAME_CLOCK:
                pass
            # keyboard events
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.messages.info(src.ui.display.take_screenshot())
                elif event.key == pygame.K_F3:
                    if RESA_GSH.start_game:
                        RESA_DH.toggle()
                elif event.key == pygame.K_p:
                    if RESA_GSH.start_game:
                        RESA_GSH.pause_game = not RESA_GSH.pause_game
                        RESA_GDH.pause_ingame_time()
                    RESA_MH.pause()
                elif event.key == pygame.K_PLUS:
                    RESA_MH.volume += .1
                elif event.key == pygame.K_MINUS:
                    RESA_MH.volume -= .1
            # mouse events
            elif event.type == pygame.MOUSEBUTTONUP:
                if RESA_GSH.start_game:
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
                    if self.game_panel_icons.collide(event.pos):
                        RESA_GSH.cursor_over_icons = True
                    else:
                        RESA_GSH.cursor_over_icons = False
            # Resa title events
            elif event.type == RESA_EH.RESA_TITLE_EVENT:
                if event.code == RESA_EH.RESA_BTN_LEAVEGAME:
                    self.leave_game()
                elif event.code == RESA_EH.RESA_BTN_SAVEGAME:
                    pass
                elif event.code == RESA_EH.RESA_QUITGAME_TRUE:
                    if RESA_GSH.start_game:
                        RESA_GSH.start_game = False
                    else:
                        RESA_GSH.exit_game = True
                elif event.code == RESA_EH.RESA_QUITGAME_FALSE:
                    RESA_GDH.pause_ingame_time()
                elif event.code == RESA_EH.RESA_BTN_STARTGAME:
                    self.map.build_world()
                    RESA_GSH.start_game = True
                    RESA_GDH.start_timer()
                elif event.code == RESA_EH.RESA_BTN_LOADGAME:
                    RESA_GDH.read_from_file(RESA_CH.save_file)
                    self.map.build_world(RESA_GDH.world_data)
                    RESA_GSH.start_game = True
                    RESA_GSH.load_game = True
                    RESA_GDH.start_timer()
                elif event.code == RESA_EH.RESA_BTN_OPTIONS:
                    RESA_GSH.options = True
                elif event.code == RESA_EH.RESA_BTN_QUITGAME:
                    RESA_GSH.exit_game = True
                elif event.code == RESA_EH.RESA_BTN_MAINMENU:
                    RESA_GSH.options = False
                elif event.code == RESA_EH.RESA_BTN_EDITOR:
                    RESA_GSH.start_editor = True
            # Resa game events
            elif event.type == RESA_EH.RESA_GAME_EVENT:
                if event.code == RESA_EH.RESA_BUILDMODE:
                    RESA_GSH.build_menu_open = False
                    RESA_GSH.build_menu = -1
                    RESA_GSH.building = not RESA_GSH.building
                elif event.code == RESA_EH.RESA_BUILD_MENU:
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

            self.messages.handle_event(event)
            if not self.messages.is_msg():
                if not RESA_GSH.start_game:
                    if RESA_GSH.options:
                        self.title_options.handle_event(event)
                    else:
                        self.title_main.handle_event(event)
                else:
                    self.debug_screen.handle_event(event)
                    # do not run game event handler on pause
                    if not RESA_GSH.pause_game and RESA_GSH.start_game:
                        self.map.handle_event(event)
                        self.game_panel_icons.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the in-game logic

        :return: None
        """
        if RESA_GSH.start_editor:
            # editor was closed and back to main menu
            if self.editor is not None:
                # restore display settings
                pygame.display.set_caption(f"{locales.get('info_welcome')} {RESA_CH.title}")
                pygame.display.set_mode((1000, 800))
                RESA_GSH.start_editor = False
                self.editor = None
            else:
                # store current display settings, create new display and start editor
                pygame.display.set_caption(f"{locales.get('info_editor_title')} {RESA_CH.title}")
                pygame.display.set_mode((1280, 960))
                self.editor = Editor()
        elif RESA_GSH.start_game:
            # current game play ended and back to main menu
            if self.game is not None and RESA_GSH.exit_game:
                RESA_MH.load()
                RESA_MH.start(RESA_CH.volume)
                RESA_GSH.start_game = False
                RESA_GSH.load_game = False
                self.game = None
            # start a game
            else:
                # update game src
                RESA_GDH.update()

                self.messages.run_logic()
                if not self.messages.is_msg():
                    if not RESA_GSH.pause_game:
                        # check for build mode
                        if RESA_GSH.building and RESA_GSH.place:
                            if self.place_building():
                                print('build')
                            else:
                                print('build not possible')

                        # update map
                        self.map.run_logic()
                        self.game_panel_icons.run_logic()

                # update debug src if activated
                if RESA_DH:
                    RESA_DH.update()
                    self.debug_screen.timer = RESA_DH.play_time
                    self.debug_screen.run_logic()
        else:
            if RESA_GSH.options:
                self.title_options.run_logic()
            else:
                self.title_main.run_logic()

        self.messages.run_logic()

    def render(self) -> None:
        """ Renders everything to the surface

        :return: None
        """
        # fill surface
        self.surface.fill(RESA_CH.COLOR_WHITE)

        # render main menu
        if not RESA_GSH.start_game:
            if RESA_GSH.options:
                self.title_options.render(self.surface)
            else:
                self.title_main.render(self.surface)
        # render game
        else:
            # render the map and blit its surface to main surface with border thickness
            self.map.render()
            pygame.Surface.blit(self.surface, self.map.get_surface(), (0, 0))
            # render the game panel
            self.game_panel_icons.render(self.surface)

            # render debug screen if activated
            if RESA_DH:
                self.debug_screen.render(self.surface)
            # render pause screen
            if RESA_GSH.pause_game:
                self.paused_screen.render(self.surface)

        # render message and info boxes
        self.messages.render(self.surface)

        # display surface
        pygame.display.flip()

    @staticmethod
    def exit():
        """ Exit routine of the game

        :return: None
        """
        pygame.quit()
        print("Bye bye!")

    def leave_game(self) -> None:
        """ Pauses in-game time and shows leaving dialog.

        :return: None
        """
        self.messages.show(locales.get('msg_cap_leavegame'), locales.get('msg_text_leavegame'),
                           pygame.event.Event(RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_QUITGAME_TRUE),
                           locales.get('btn_msg_yes'),
                           pygame.event.Event(RESA_EH.RESA_TITLE_EVENT, code=RESA_EH.RESA_QUITGAME_FALSE),
                           locales.get('btn_msg_no'))
        RESA_GDH.pause_ingame_time()

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
