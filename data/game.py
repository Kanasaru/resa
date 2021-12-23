""" This module provides the game

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.handlers.sound import SoundHandler
from data.settings import conf
from datetime import datetime
import pygame
import logging
import data.eventcodes as ecodes
from data.interfaces.debugscreen import DebugScreen
from data.interfaces.gamepanel import GamePanel
from data.interfaces.pausescreen import GamePausedScreen
from data.handlers.spritesheet import SpriteSheet, SpriteSheetHandler
from data.world.map import Map
from data.handlers.debug import DebugHandler
from data.handlers.gamedata import GameDataHandler
from data.handlers.music import Music
from data.handlers.msg import Message


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

        # set handler
        self.debug_handler = DebugHandler()
        self.game_data_handler = GameDataHandler()
        self.game_data_handler.game_time_speed = conf.game_speed
        self.music = Music()
        self.music.load()
        self.sounds = SoundHandler()

        # screen settings, build screens and panels
        self.surface = pygame.display.get_surface()
        self.border_thickness = conf.map_border_thickness
        self.border_color = conf.COLOR_WHITE
        # debug screen
        self.debug_screen = DebugScreen()
        self.debug_screen.add('FPS', self.clock.get_fps)
        self.debug_screen.add('Version', lambda: conf.version)
        self.debug_screen.add('Date', lambda: datetime.now().strftime('%A, %d. %B %Y'))
        self.debug_screen.add('In-Game time', self.game_data_handler.get_game_time)
        # game panel
        game_panel_sheet_handler = SpriteSheetHandler()
        buttons = SpriteSheet(conf.sp_menu_btn_key, conf.sp_menu_btn, conf.sp_menu_btn_size)
        buttons.colorkey = (1, 0, 0)
        game_panel_sheet_handler.add(buttons)
        self.game_panel = GamePanel(game_panel_sheet_handler, conf.sp_menu_btn_key)
        # messages
        self.messages = Message(game_panel_sheet_handler, conf.sp_menu_btn_key)
        self.messages.top = self.game_panel.rect.height + self.border_thickness * 3
        # pause screen
        self.paused_screen = GamePausedScreen(pygame.Rect(
            (0, self.game_panel.rect.height),
            (conf.resolution[0], conf.resolution[1] - self.game_panel.rect.height)))

        # loading map
        self.map = None
        self.load_map()

        # timer
        pygame.time.set_timer(ecodes.RESA_AUTOSAVE_EVENT, conf.autosave_interval)

        # start the game loop
        self.loop()

    def load_map(self) -> None:
        """ Loads the map from file or builds a new one

        :return: None
        """
        # map instance with shrinked surface size to provide border and room for game panel
        surface_width = conf.resolution[0] - self.border_thickness * 2
        surface_height = conf.resolution[1] - self.game_panel.rect.height - self.border_thickness * 2
        self.map = Map((surface_width, surface_height))

        if self.map_load:
            # load world from file
            self.game_data_handler.read_from_file(conf.save_file)
            self.map.build_world(self.game_data_handler.world_data)
        else:
            # build a new world
            self.map.build_world()

        # update resources in game panel
        self.game_panel.resources = self.game_data_handler.resources

    def loop(self) -> None:
        """ in-game loopp

        :return: None
        """
        self.game_data_handler.start_timer()
        self.music.start(conf.volume)

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
                    self.debug_handler.toggle()
                elif event.key == pygame.K_p:
                    self.pause_game = not self.pause_game
                    self.game_data_handler.pause_ingame_time()
                    self.music.pause()
                elif event.key == pygame.K_PLUS:
                    self.music.volume += .1
                elif event.key == pygame.K_MINUS:
                    self.music.volume -= .1
                else:
                    pass
            elif event.type == ecodes.RESA_AUTOSAVE_EVENT and conf.autosave:
                self.save_game(True)
            elif event.type == ecodes.RESA_MUSIC_ENDED_EVENT:
                if len(self.music.playlist) > 0:
                    self.music.load_next()
                else:
                    self.music.refill()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pass
                elif event.button == 2:
                    pass
                else:
                    pass
            elif event.type == ecodes.RESA_TITLE_EVENT:
                if event.code == ecodes.RESA_BTN_LEAVEGAME:
                    self.leave_game()
                elif event.code == ecodes.RESA_BTN_SAVEGAME:
                    self.save_game()
                elif event.code == ecodes.RESA_QUITGAME_TRUE:
                    self.exit_game = True
                elif event.code == ecodes.RESA_QUITGAME_FALSE:
                    self.game_data_handler.pause_ingame_time()
                else:
                    pass
            else:
                pass

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
        # update game data
        self.game_data_handler.update()

        self.messages.run_logic()
        if not self.messages.is_msg():
            if not self.pause_game:
                # update map
                self.map.run_logic()
            # update game panel
            self.game_panel.run_logic()

        # update debug data if activated
        if self.debug_handler:
            self.debug_handler.update()
            self.debug_screen.timer = self.debug_handler.play_time
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
        if self.debug_handler:
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
        self.sounds.play('screenshot')
        filename = f'{conf.screenshot_path}screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
        pygame.image.save(pygame.display.get_surface(), filename)
        self.messages.info(f'Took screenshot: {filename}')
        logging.info('Took screenshot')

    def save_game(self, auto_save: bool = False) -> None:
        """ Saves the game into its save-file.

        :return: None
        """
        self.game_data_handler.world_data = (self.map.rect, self.map.get_raw_fields(), self.map.get_raw_trees())
        self.game_data_handler.save_to_file(conf.save_file)
        if auto_save:
            text = 'Game saved automatically!'
        else:
            text = 'Game saved!'
        self.messages.info(text)
        logging.info(text)

    def leave_game(self) -> None:
        """ Pauses in-game time and shows leaving dialog.

        :return: None
        """
        self.messages.show('Leavinvg the game...', 'Are you sure?',
                           pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_QUITGAME_TRUE),
                           'Yes',
                           pygame.event.Event(ecodes.RESA_TITLE_EVENT, code=ecodes.RESA_QUITGAME_FALSE),
                           'No')
        self.game_data_handler.pause_ingame_time()
