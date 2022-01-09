""" This module provides the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: CC-BY-SA-4.0
"""
import src.locales as locales
from src.handler import conf
from datetime import datetime
import pygame
import logging
import src.handler
from src.ui.screens import DebugScreen, GamePausedScreen
from src.ui.panels import GamePanel
from src.world.map import Map
from src.ui.form import MessageHandler


class Game(object):
    def __init__(self, load: bool = False) -> None:
        """ Initializes the game

        :param load: load game from file if true
        """
        # event handling varibales
        self.exit_game = False
        self.map_load = load
        self.pause_game = False

        # set timers and clocks
        self.clock = pygame.time.Clock()

        # screen settings, build screens and panels
        self.surface = pygame.display.get_surface()
        self.border_thickness = conf.map_border_thickness
        self.border_color = conf.COLOR_WHITE
        # debug screen
        self.debug_screen = DebugScreen()
        self.debug_screen.add(locales.get('info_fps'), self.clock.get_fps)
        self.debug_screen.add(locales.get('info_version'), lambda: conf.version)
        self.debug_screen.add(locales.get('info_date'), lambda: datetime.now().strftime("%A, %d. %B %Y"))
        self.debug_screen.add(locales.get('info_ingame_time'), src.handler.hdl_gamedata.get_game_time)
        # game panel
        self.game_panel = GamePanel(src.handler.hdl_sh_titles, conf.sp_menu_btn_key)
        # messages
        self.messages = MessageHandler(src.handler.hdl_sh_titles, conf.sp_menu_btn_key)
        self.messages.top = self.game_panel.rect.height + self.border_thickness * 3
        # pause screen
        self.paused_screen = GamePausedScreen(pygame.Rect(
            (0, self.game_panel.rect.height),
            (pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height() - self.game_panel.rect.height)))

        # loading map
        self.map = None
        self.load_map()

        # timer
        pygame.time.set_timer(src.handler.RESA_AUTOSAVE_EVENT, conf.autosave_interval)

        # start the game loop
        self.loop()

    def load_map(self) -> None:
        """ Loads the map from file or builds a new one

        :return: None
        """
        # map instance with shrinked surface size to provide border and room for game panel
        surface_width = pygame.display.get_surface().get_width() - self.border_thickness * 2
        surface_height = pygame.display.get_surface().get_height() - self.game_panel.rect.height - self.border_thickness * 2
        self.map = Map((surface_width, surface_height))

        if self.map_load:
            # load world from file
            src.handler.hdl_gamedata.read_from_file(conf.save_file)
            self.map.build_world(src.handler.hdl_gamedata.world_data)
        else:
            # build a new world
            self.map.build_world()

        # update resources in game panel
        self.game_panel.resources = src.handler.hdl_gamedata.resources

    def loop(self) -> None:
        """ in-game loopp

        :return: None
        """
        src.handler.hdl_gamedata.start_timer()
        src.handler.hdl_music.start(conf.volume)

        while not self.exit_game:
            self.clock.tick(conf.fps)
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
                    src.handler.hdl_debug.toggle()
                elif event.key == pygame.K_p:
                    self.pause_game = not self.pause_game
                    src.handler.hdl_gamedata.pause_ingame_time()
                    src.handler.hdl_music.pause()
                elif event.key == pygame.K_PLUS:
                    src.handler.hdl_music.volume += .1
                elif event.key == pygame.K_MINUS:
                    src.handler.hdl_music.volume -= .1
            elif event.type == src.handler.RESA_AUTOSAVE_EVENT and conf.autosave:
                self.save_game(True)
            elif event.type == src.handler.RESA_MUSIC_ENDED_EVENT:
                if len(src.handler.hdl_music.playlist) > 0:
                    src.handler.hdl_music.load_next()
                else:
                    src.handler.hdl_music.refill()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # cursor in map?
                    cursor_x = event.pos[0] - self.map.rect.x - self.border_thickness
                    cursor_y = event.pos[1] - self.map.rect.y - self.game_panel.rect.height - self.border_thickness
                    if cursor_x >= 0 and cursor_y >= 0:
                        cursor_on_map = True
                    else:
                        cursor_on_map = False

                    if cursor_on_map and not self.messages.is_msg():
                        print(self.map.world.grid.pos_in_iso_grid_field((cursor_x, cursor_y)))
                elif event.button == 2:
                    pass
            elif event.type == src.handler.RESA_TITLE_EVENT:
                if event.code == src.handler.RESA_BTN_LEAVEGAME:
                    self.leave_game()
                elif event.code == src.handler.RESA_BTN_SAVEGAME:
                    self.save_game()
                elif event.code == src.handler.RESA_QUITGAME_TRUE:
                    self.exit_game = True
                elif event.code == src.handler.RESA_QUITGAME_FALSE:
                    src.handler.hdl_gamedata.pause_ingame_time()

            # push event into title and map event handling
            self.debug_screen.handle_event(event)
            self.messages.handle_event(event)
            if not self.messages.is_msg():
                self.game_panel.handle_event(event)
                # do not run game event handler on pause
                if not self.pause_game:
                    self.map.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the in-game logic

        :return: None
        """
        # update game src
        src.handler.hdl_gamedata.update()

        self.messages.run_logic()
        if not self.messages.is_msg():
            if not self.pause_game:
                # update map
                self.map.run_logic()
            # update game panel
            self.game_panel.run_logic()

        # update debug src if activated
        if src.handler.hdl_debug:
            src.handler.hdl_debug.update()
            self.debug_screen.timer = src.handler.hdl_debug.play_time
            self.debug_screen.run_logic()

    def render(self) -> None:
        """ Renders everything to the surface

        :return: None
        """
        # fill surface, will be the border color
        self.surface.fill(self.border_color)

        # render the map and blit its surface to main surface with border thickness
        self.map.render()
        pos_x = self.border_thickness
        pos_y = self.game_panel.rect.height + self.border_thickness
        pygame.Surface.blit(self.surface, self.map.get_surface(), (pos_x, pos_y))

        # render message and info boxes
        self.messages.render(self.surface)

        # render the game panel
        self.game_panel.render(self.surface)

        # render debug screen if activated
        if src.handler.hdl_debug:
            self.debug_screen.render(self.surface)

        # render pause screen
        if self.pause_game:
            self.paused_screen.render(self.surface)

        # display surface
        pygame.display.flip()

    def take_screenshot(self) -> None:
        """ Saves the current screen as an image.

        :return: None
        """
        src.handler.hdl_sound.play('screenshot')
        filename = f'{conf.screenshot_path}screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpeg'
        pygame.image.save(pygame.display.get_surface(), filename)
        self.messages.info(f"{locales.get('info_screenshot')}: {filename}")
        logging.info('Took screenshot')

    def save_game(self, auto_save: bool = False) -> None:
        """ Saves the game into its save-file.

        :return: None
        """
        src.handler.hdl_gamedata.world_data = (self.map.rect, self.map.get_raw_fields(), self.map.get_raw_trees())
        src.handler.hdl_gamedata.save_to_file(conf.save_file)
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
                           pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_QUITGAME_TRUE),
                           locales.get('btn_msg_yes'),
                           pygame.event.Event(src.handler.RESA_TITLE_EVENT, code=src.handler.RESA_QUITGAME_FALSE),
                           locales.get('btn_msg_no'))
        src.handler.hdl_gamedata.pause_ingame_time()
