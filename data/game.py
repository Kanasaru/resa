""" This module provides classes to load world

:project: resa
:source: https://github.com/Kanasaru/resa
:license: GNU General Public License v3
"""

from data.settings import conf
from datetime import datetime
import pygame
import data.eventcodes as ecodes
from data.interfaces.debugscreen import DebugScreen
from data.interfaces.gamepanel import GamePanel
from data.handlers.spritesheet import SpriteSheet, SpriteSheetHandler
from data.world.map import Map
from data.handlers.debug import DebugHandler
from data.handlers.gamedata import GameDataHandler


class Game(object):
    def __init__(self, load: bool = False) -> None:
        """ Initializes the game

        :param load: load game from file if true
        """
        # event handling varibales
        self.exit_game = False
        self.map_load = load
        self.screenshot = False

        # set timers and clocks
        self.clock = pygame.time.Clock()

        # set handler
        self.debug_handler = DebugHandler()
        self.game_data_handler = GameDataHandler()
        self.game_data_handler.game_time_speed = conf.game_speed

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

        # loading map
        self.map = None
        self.load_map()

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
        """ in-game loop

        :return: None
        """
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
                self.exit_game = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    self.screenshot = True
                elif event.key == pygame.K_F3:
                    self.debug_handler.toggle()
                else:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pass
                if event.button == 2:
                    pass
            elif event.type == ecodes.RESA_TITLE_EVENT:
                if event.code == ecodes.RESA_STOPGAME:
                    self.exit_game = True
                elif event.code == ecodes.RESA_SAVEGAME:
                    self.game_data_handler.world_data = (
                        self.map.rect,
                        self.map.get_raw_fields(),
                        self.map.get_raw_trees()
                    )
                    self.game_data_handler.save_to_file(conf.save_file)
                else:
                    pass
            else:
                pass

            # push event into title and map event handling
            self.debug_screen.handle_event(event)
            self.game_panel.handle_event(event)
            self.map.handle_event(event)

    def run_logic(self) -> None:
        """ Runs the in-game logic

        :return: None
        """
        # update game data
        self.game_data_handler.update()

        # update debug data if activated
        if self.debug_handler:
            self.debug_handler.update()
            self.debug_screen.timer = self.debug_handler.play_time
            self.debug_screen.run_logic()

        # update game panel
        self.game_panel.run_logic()

        # update map
        self.map.run_logic()

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

        # render the game panel
        self.game_panel.render(self.surface)

        # render debug screen if activated
        if self.debug_handler:
            self.debug_screen.render(self.surface)

        # screenshot
        if self.screenshot:
            self.take_screenshot()

        # display surface
        pygame.display.flip()

    def take_screenshot(self):
        pygame.image.save(pygame.display.get_surface(), f'saves/screenshot_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
        self.screenshot = False
