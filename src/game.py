""" This module provides the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import src.locales as locales
from datetime import datetime
import pygame
import logging
from src.handler import RESA_CH, RESA_SSH, RESA_GDH, RESA_GSH, RESA_SH, RESA_MH, RESA_DH, RESA_EH
from src.ui.screens import DebugScreen, GamePausedScreen
from src.ui.panels import GamePanel
from src.world.map import Map
from src.ui.form import MessageHandler
from src.world.entities.building import Building


class Game(object):
    def __init__(self, load: bool = False) -> None:
        """ Initializes the game

        :param load: load game from file if true
        """
        # event handling varibales
        RESA_GSH.exit_game = False
        RESA_GSH.map_load = load
        RESA_GSH.pause_game = False
        RESA_GSH.building = False

        # set timers and clocks
        self.clock = pygame.time.Clock()

        # screen settings, build screens and panels
        self.surface = pygame.display.get_surface()
        self.border_thickness = RESA_CH.map_border_thickness
        self.border_color = RESA_CH.COLOR_WHITE
        # debug screen
        self.debug_screen = DebugScreen()
        self.debug_screen.add(locales.get('info_fps'), self.clock.get_fps)
        self.debug_screen.add(locales.get('info_version'), lambda: RESA_CH.version)
        self.debug_screen.add(locales.get('info_date'), lambda: datetime.now().strftime("%A, %d. %B %Y"))
        self.debug_screen.add(locales.get('info_ingame_time'), RESA_GDH.get_game_time)
        # game panel
        self.game_panel = GamePanel(RESA_SSH, RESA_CH.sp_menu_btn_key)
        # messages
        self.messages = MessageHandler(RESA_SSH, RESA_CH.sp_menu_btn_key)
        self.messages.top = self.game_panel.rect.height + self.border_thickness * 3
        # pause screen
        self.paused_screen = GamePausedScreen(pygame.Rect(
            (0, self.game_panel.rect.height),
            (pygame.display.get_surface().get_width(),
             pygame.display.get_surface().get_height() - self.game_panel.rect.height)))

        # loading map
        self.map = None
        self.map_shift = (self.border_thickness, self.game_panel.rect.height + self.border_thickness)
        self.load_map()

        # timer
        pygame.time.set_timer(RESA_EH.RESA_AUTOSAVE_EVENT, RESA_CH.autosave_interval)

        # start the game loop
        self.loop()

    def load_map(self) -> None:
        """ Loads the map from file or builds a new one

        :return: None
        """
        # map instance with shrinked surface size to provide border and room for game panel
        surface_width = pygame.display.get_surface().get_width() - self.border_thickness * 2
        surface_height = pygame.display.get_surface().get_height() - self.game_panel.rect.height - self.border_thickness * 2
        self.map = Map((surface_width, surface_height), self.map_shift)

        if RESA_GSH.map_load:
            # load world from file
            RESA_GDH.read_from_file(RESA_CH.save_file)
            self.map.build_world(RESA_GDH.world_data)
        else:
            # build a new world
            self.map.build_world()

        # update resources in game panel
        self.game_panel.resources = RESA_GDH.resources

    def loop(self) -> None:
        """ in-game loopp

        :return: None
        """
        RESA_GDH.start_timer()
        RESA_MH.start(RESA_CH.volume)

        while not RESA_GSH.exit_game:
            self.clock.tick(RESA_CH.fps)
            self.handle_events()
            self.run_logic()
            self.render()

    def handle_events(self) -> None:
        """ Handles all in-game events

        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.leave_game()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.take_screenshot()
                elif event.key == pygame.K_F3:
                    RESA_DH.toggle()
                elif event.key == pygame.K_p:
                    RESA_GSH.pause_game = not RESA_GSH.pause_game
                    RESA_GDH.pause_ingame_time()
                    RESA_MH.pause()
                elif event.key == pygame.K_PLUS:
                    RESA_MH.volume += .1
                elif event.key == pygame.K_MINUS:
                    RESA_MH.volume -= .1
            elif event.type == RESA_EH.RESA_AUTOSAVE_EVENT and RESA_CH.autosave:
                self.save_game(True)
            elif event.type == RESA_EH.RESA_MUSIC_ENDED_EVENT:
                if len(RESA_MH.playlist) > 0:
                    RESA_MH.load_next()
                else:
                    RESA_MH.refill()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # cursor in map?
                    cursor_x = event.pos[0] - self.map.rect.x - self.map_shift[0]
                    cursor_y = event.pos[1] - self.map.rect.y - self.map_shift[1]
                    if cursor_x >= 0 and cursor_y >= 0:
                        cursor_on_map = True
                    else:
                        cursor_on_map = False

                    if cursor_on_map and not self.messages.is_msg():
                        print(self.map.world.grid.pos_in_iso_grid_field((cursor_x, cursor_y)))
                        # build mode
                        if RESA_GSH.building:
                            RESA_GSH.place = True
                            RESA_GSH.place_on = self.map.world.grid.pos_in_iso_grid_field((cursor_x, cursor_y))
                elif event.button == 2:
                    pass
            elif event.type == RESA_EH.RESA_TITLE_EVENT:
                if event.code == RESA_EH.RESA_BTN_LEAVEGAME:
                    self.leave_game()
                elif event.code == RESA_EH.RESA_BTN_SAVEGAME:
                    self.save_game()
                elif event.code == RESA_EH.RESA_QUITGAME_TRUE:
                    RESA_GSH.exit_game = True
                elif event.code == RESA_EH.RESA_QUITGAME_FALSE:
                    RESA_GDH.pause_ingame_time()
            elif event.type == RESA_EH.RESA_GAME_EVENT:
                if event.code == RESA_EH.RESA_BUILDMODE:
                    RESA_GSH.building = not RESA_GSH.building

            # push event into title and map event handling
            self.debug_screen.handle_event(event)
            self.messages.handle_event(event)
            if not self.messages.is_msg():
                self.game_panel.handle_event(event)
                # do not run game event handler on pause
                if not RESA_GSH.pause_game:
                    self.map.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the in-game logic

        :return: None
        """
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
            # update game panel
            self.game_panel.run_logic()

        # update debug src if activated
        if RESA_DH:
            RESA_DH.update()
            self.debug_screen.timer = RESA_DH.play_time
            self.debug_screen.run_logic()

    def render(self) -> None:
        """ Renders everything to the surface

        :return: None
        """
        # fill surface, will be the border color
        self.surface.fill(self.border_color)

        # render the map and blit its surface to main surface with border thickness
        self.map.render()
        pygame.Surface.blit(self.surface, self.map.get_surface(), self.map_shift)

        # render message and info boxes
        self.messages.render(self.surface)

        # render the game panel
        self.game_panel.render(self.surface)

        # render debug screen if activated
        if RESA_DH:
            self.debug_screen.render(self.surface)

        # render pause screen
        if RESA_GSH.pause_game:
            self.paused_screen.render(self.surface)

        # display surface
        pygame.display.flip()

    def take_screenshot(self) -> None:
        """ Saves the current screen as an image.

        :return: None
        """
        RESA_SH.play('screenshot')
        filename = f'{RESA_CH.screenshot_path}screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpeg'
        pygame.image.save(pygame.display.get_surface(), filename)
        self.messages.info(f"{locales.get('info_screenshot')}: {filename}")
        logging.info('Took screenshot')

    def save_game(self, auto_save: bool = False) -> None:
        """ Saves the game into its save-file.

        :return: None
        """
        RESA_GDH.world_data = (self.map.rect, self.map.get_raw_fields(), self.map.get_raw_trees())
        RESA_GDH.save_to_file(RESA_CH.save_file)
        if auto_save:
            text = locales.get('info_autosave')
        else:
            text = locales.get('info_save')
        self.messages.info(text)
        logging.info(text)

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
                if raw_field.solid:
                    raw_field = self.map.world.grid_fields[neighbors.topleft]
                    if raw_field.solid:
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
                new_building = Building(raw_field.rect.midbottom,
                                        pygame.image.load('res/sprites/entities/build_3x3_test.png').convert(), 1)
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
                new_building = Building(raw_field.rect.midbottom,
                                        pygame.image.load('res/sprites/entities/build_3x3_test.png').convert(), 2)
                self.map.world.grid_fields[RESA_GSH.place_on.key].sprite = new_building
            # 3x3
            elif x == y == 3:
                self.map.world.grid_fields[RESA_GSH.place_on.key].sprite = None
                for rawval in neighbors.all:
                    self.map.world.grid_fields[rawval].sprite = None
                    self.map.world.grid_fields[rawval].building = True

                raw_field = self.map.world.grid_fields[neighbors.bottom]
                new_building = Building(raw_field.rect.midbottom,
                                        pygame.image.load('res/sprites/entities/build_3x3_test.png').convert(), 3)
                self.map.world.grid_fields[RESA_GSH.place_on.key].sprite = new_building

        # reset state
        RESA_GSH.place = False
        RESA_GSH.place_on = None

        return build
